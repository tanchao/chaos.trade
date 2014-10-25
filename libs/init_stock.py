import urllib2
import time

def download_ystock_history_data(symbol='000001.sz'):
    ''' download whole history data from yahoo finance '''
    req_url = 'http://table.finance.yahoo.com/table.csv?s=' + symbol
    try:
        res = urllib2.urlopen(req_url)
    except urllib2.URLError, e:
        print 'you got an error with the code', e.code, 'for symbol:', symbol
    else:
        body = res.read()
        print symbol + ' downloaded'
        with open(symbol, 'w') as sfile:
            sfile.write(body)
        print symbol + ' stored'

def init_basic_history_data_from_ystock():
    ''' download all default csv files from yahoo finance '''
    print 'init_basic_history_data_from_ystock started'
    with open('stock_list') as sl:
        stocks = sl.readlines()
        for stock in stocks:
            symbol = stock[:-1]
            download_ystock_history_data(symbol)
    print 'init_basic_history_data_from_ystock done'

if __name__ == '__main__':
    init_basic_history_data_from_ystock()
