import urllib2
import json

import config
import models.stocks

jd = {'status': 404, 'continstallent': []}

'''
import controllers.stock as cs
cs.init_stocks_from_csv()
'''


def init_stocks_from_csv():
    try:
        # print config.ROOT
        file_ = config.ROOT + 'static/docs/data/GOOG.ORI.csv'
        csv_ = open(file_, 'r')
        lines_ = csv_.readlines()
        lines_.pop(0)
        lines_.reverse()
        d_ = cols_ = []
        ema5 = ema10 = ema12 = ema20 = ema26 = ema52 = ema60 = 0
        for line_ in lines_:
            cols_ = line_[:-1].split(',')
            adj_ = float(cols_[-1])
            ema5 = ema5 * 4 / 6 + adj_ * 2 / 6
            ema10 = ema10 * 9 / 11 + adj_ * 2 / 11
            ema12 = ema12 * 11 / 13 + adj_ * 2 / 13
            ema20 = ema20 * 19 / 21 + adj_ * 2 / 21
            ema26 = ema26 * 25 / 27 + adj_ * 2 / 27
            ema52 = ema52 * 51 / 53 + adj_ * 2 / 53
            ema60 = ema60 * 59 / 61 + adj_ * 2 / 61
            cols_.append(ema5)
            cols_.append(ema10)
            cols_.append(ema12)
            cols_.append(ema20)
            cols_.append(ema26)
            cols_.append(ema52)
            cols_.append(ema60)
            models.stocks.new_stock('GOOG', cols_[0], float(cols_[1]), float(cols_[2]), float(cols_[3]), float(cols_[4]), float(cols_[5]), float(cols_[6]), cols_[7], cols_[8], cols_[9], cols_[10], cols_[11], cols_[12], cols_[13])
            d_.append(cols_)
        return d_
    except Exception, e:
        print e
    finally:
        csv_.close()


def get_stock_from_csv(file_name_):
    try:
        csv_ = open(file_name_)
        d_ = []
        lines_ = csv_.readlines()
        for line_ in lines_[0].split('\r'):
            if line_.startswith('Date'):
                continue
            cols_ = line_.split(',')
            d_.append(cols_)
        return d_[:250]
    except:
        print 'error while get_stock_from_csv'


def get_ema5_from_csv(file_name_):
    try:
        csv_ = open(file_name_)
        d_ = []
        lines_ = csv_.readlines()
        for line_ in lines_[0].split('\r'):
            if line_.startswith('Date'):
                continue
            cols_ = line_.split(',')
            d_.append([int(cols_[0]), float(cols_[2])])
        return {'data': d_[:250]}
    except:
        print 'error while get_ema5_from_csv'


def get_stock_code(id_):
    ''' translate '''
    if id_.startswith('sh') or id_.startswith('sz'):
        return id_[2:]
    if id_.endswith('.sh') or id_.endswith('.sz'):
        return id_[:-3]


def get_stock_market(id_):
    if 'sh' in id_:
        return 'SH'
    if 'sz' in id_:
        return 'SZ'
    return 'TBD'


def update_rt_sd(id_):
    ''' get real time stock data from sina api
            @id stock code e.g sh600031, sz000157
            return market data into database '''
    url_ = config.RT_SD_URL + id_  # http://hq.sinajs.cn/list=sz000157


def update_his_sd(id_):
    ''' get history stock data from yahoo api
            @id stock code e.g 600031.sh, 000157.sz
            get csv file for the history data
            return market data into data base '''
    # http://table.finance.yahoo.com/table.csv?s=000157.sz
    url_ = config.HIS_SD_URL + id_
    re_ = urllib2.urlopen(url_)
    for record_ in re_.readlines():
        if record_.startswith('Date'):
            continue
        records = record_.split(',')
        date_ = records[0]
        open_ = records[1]
        high_ = records[2]
        low_ = records[3]
        close_ = records[4]
        volume_ = records[5]
        adjclose_ = records[6]
        code_ = get_stock_code(id_)
        mkt_ = get_stock_market(id_)
        models.stock_model.new_stock(
            soricode=id_, scode=code_, smarket=mkt_, sdate=date_,
            sopen=open_, sclose=close_, shigh=high_, slow=low_, svol=volume_, sadjclose=adjclose_)
