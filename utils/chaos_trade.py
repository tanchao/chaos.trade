#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from datetime import date, timedelta

_TODAY_ = date.today().strftime('%y%m%d')
_YESTERDAY_ = (date.today() - timedelta(1)).strftime('%y%m%d')

__author__ = 'tanchao'
__version__ = '0.0.1'

try:
    # py3
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
except ImportError:
    # py2
    from urllib2 import Request, urlopen
    from urllib import urlencode


def _request_sina(symbol):
    url = 'http://hq.sinajs.cn/list={}'.format(symbol.lower())
    try:
        req = Request(url)
        res = urlopen(req)
        return res.read()
    except Exception:
        return ''


def _get_stock_list():
    stock_list_path = 'static/stock.symbols.txt'
    if not os.path.isfile(stock_list_path):
        stock_list_path = 'stock.symbols.txt'
    stock_list_file = stock_list_path
    stock_list = []
    count = 0
    if os.path.isfile(stock_list_file):
        with open(stock_list_file, 'r') as slf:
            for line in slf.readlines():
                count += 1
                if line.endswith('\n'):
                    stock_list.append(line[:-1])
                else:
                    stock_list.append(line)
        stock_list.sort()
    else:
        print('!!!error: cannot find ' + stock_list_file)
    return stock_list


def _calc_wave(symbol):
    res = _request_sina(symbol)
    if res and not '""' in res:
        symboll = res[res.index('"'):res.rindex('"')].split(',')
        price = float(symboll[3])
        high = float(symboll[4])
        low = float(symboll[5])
        high_low_wave = (high - low) / high + 0.01
        price_wave = abs(price - (high + low) / 2) / float(price) + 0.002
        print('+++ high_low: {} price: {} +++'.format(high_low_wave, price_wave))
        return high_low_wave, price_wave
    else:
        print('!!!error while get response for symbol ' + symbol)
        print(res)
        return [0, 0]


def _chaos_selector(close_rate, high_low_wave, price_wave, stock_list):
    selected = {}
    for stock in stock_list:
        res = _request_sina(stock)
        if not (not res or '""' in res):  # not empty response
            stock_str = res[res.index('"'):res.rindex('"')]
            stock_data = stock_str.split(',')
            if len(stock_data) < 32:  # stock data length check
                print(stock + ' response is not enough: ' + stock_str)
                continue
            else:
                ds = dict(
                    name=stock_data[0],
                    tstart=float(stock_data[1]),
                    yend=float(stock_data[2]),
                    price=float(stock_data[3]),
                    thigh=float(stock_data[4]),
                    tlow=float(stock_data[5]),
                    tdate=stock_data[30],
                    ttime=stock_data[31],
                )  # init stock dictionary with necessary info only
                if 0 in ds.values():
                    continue  # suspend
                elif ((ds['thigh'] - ds['yend']) / ds['yend']) > 0.098:
                    continue  # limit-up
                elif 'ST' in ds['name'] and ((ds['thigh'] - ds['yend']) / ds['yend']) > 0.048:
                    continue  # st limit-up
                elif (ds['price'] - ds['tstart']) / ds['tstart'] > 0.04:
                    continue  # up too much
                elif ds['price'] == ds['tstart'] or ds['thigh'] == ds['tlow']:
                    continue  # not in up trend
                elif (ds['price'] - ds['tstart']) / (ds['thigh'] - ds['tlow']) < close_rate:
                    continue  # not close enough
                elif (ds['thigh'] - ds['tlow']) / ds['thigh'] > high_low_wave:
                    continue  # high low wave too large
                elif abs(ds['tstart'] - ds['tlow']) / ds['tstart'] > price_wave:
                    continue  # start price wave too large
                elif abs(ds['price'] - ds['thigh']) / ds['price'] > price_wave:
                    continue  # end price wave too large
                else:  # stock selected
                    print('*** {} : {}'.format(stock, ds))
                    selected[stock] = ds
        else:
            # print(stock + ' response is empty')
            continue
    return selected


def chaos(market='all', rate=0.9):
    SH_INDEX = 'sh000001'  # Shanghai Market
    SZ_INDEX = 'sz399001'  # Shenzhen Market
    SC_INDEX = 'sz399006'  # Shenchuang Market
    SZ_START = 'sz000001'
    SC_START = 'sz300001'
    CLOSE_RATE = rate
    market = market.lower()

    stock_list = _get_stock_list()
    if len(stock_list) < 2000:
        errMsg = '!!!error stock symbols not ok'
        print(errMsg)
        return errMsg
    chaos_stock = {}

    if market in ('all', 'sh'):  # Shanghai
        sh_stock_list = stock_list[:stock_list.index(SZ_START)]
        sh_high_low_wave, sh_price_wave = _calc_wave(SH_INDEX)
        sh_stock = _chaos_selector(CLOSE_RATE, sh_high_low_wave, sh_price_wave, sh_stock_list)
        chaos_stock.update(sh_stock)
    if market in ('all', 'sz'):  # Shenzhen
        sz_stock_list = stock_list[stock_list.index(SZ_START):stock_list.index(SC_START)]
        sz_high_low_wave, sz_price_wave = _calc_wave(SZ_INDEX)
        sz_stock = _chaos_selector(CLOSE_RATE, sz_high_low_wave, sz_price_wave, sz_stock_list)
        chaos_stock.update(sz_stock)
    if market in ('all', 'sc'):  # Shenchuang
        sc_stock_list = stock_list[stock_list.index(SC_START):]
        sc_high_low_wave, sc_price_wave = _calc_wave(SC_INDEX)
        sc_stock = _chaos_selector(CLOSE_RATE, sc_high_low_wave, sc_price_wave, sc_stock_list)
        chaos_stock.update(sc_stock)

    # save selected trades
    sf = _TODAY_ + '.log'
    with open(sf, 'w') as sfh:
        for stock in chaos_stock:
            sfh.write(str(stock) + ' : ' + str(chaos_stock[stock]) + '\n')
    return chaos_stock


def valid_chaos():
    f = _YESTERDAY_ + '.log'
    with open(f, 'r') as fh:
        pass


def chaos_30():
    selected = {}
    symbol30 = 'sz399006'
    res30 = _request_sina(symbol30)
    print(res30)
    lsymbol30 = res30[res30.index('"'):res30.rindex('"')].split(',')
    _hl_gap_ = (float(lsymbol30[4]) - float(lsymbol30[5])) / float(lsymbol30[4]) + 0.02
    _se_gap_ = abs(float(lsymbol30[3]) - (float(lsymbol30[4]) + float(lsymbol30[5])) / 2) / float(lsymbol30[3]) + 0.002
    print('high-low is {}, start-end is {}'.format(_hl_gap_, _se_gap_))
    for x in range(1, 1000):
        symbol = 'sz30' + "%04d" % x  # '30' + '0001'
        pain_res = _request_sina(symbol)
        if pain_res and not '""' in pain_res:
            str_symbol = pain_res[pain_res.index('"'):pain_res.rindex('"')]
            # print(str_symbol)
            list_symbol = str_symbol.split(',')
            if not len(list_symbol) > 5:
                break
            ds = dict(
                name=list_symbol[0],
                tstart=float(list_symbol[1]),
                yend=float(list_symbol[2]),
                price=float(list_symbol[3]),
                thigh=float(list_symbol[4]),
                tlow=float(list_symbol[5]),
                tdate=list_symbol[30],
                ttime=list_symbol[31],
            )
            # _hl_gap_ = 0.05
            # _se_gap_ = 0.005
            '''
             and
                    abs(ds['tstart'] - ds['tlow']) / ds['tstart'] < _se_gap_ and
                    abs(ds['tend'] - ds['thigh']) / ds['thigh'] < _se_gap_
                    (ds['thigh'] - ds['tlow']) / ds['thigh'] < _hl_gap_ and
                    ds['tend'] > ds['tstart'] and
            '''
            if 0 not in ds.values() and \
                            ds['thigh'] > ds['tlow'] and \
                                    (ds['price'] - ds['tstart']) / (ds['thigh'] - ds['tlow']) > 0.7 and \
                                    abs(ds['tstart'] - ds['tlow']) / ds['tstart'] < _se_gap_ and \
                                    (ds['thigh'] - ds['tlow']) / ds['thigh'] < _hl_gap_ and \
                                    abs(ds['price'] - ds['thigh']) / ds['price'] < _se_gap_:
                print('{} : {}'.format(symbol, ds))
                selected[symbol] = ds
        else:
            continue  # no handler for None type yet
    print(len(selected))
    # for s in selected:
    # print(s, selected[s]['name'])
    sf = _TODAY_ + '.log'
    with open(sf, 'w') as sfh:
        sfh.write(str(selected))
    return selected


if '__main__' == __name__:
    args = sys.argv
    if len(args) == 3:  # for local
        chaos(args[1], args[2])
    else:
        chaos()