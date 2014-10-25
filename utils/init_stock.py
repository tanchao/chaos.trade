import urllib2

def download_ystock_history_data(symbol='000001.sz'):
    ''' download whole history data from yahoo finance '''
    req_url = 'http://table.finance.yahoo.com/table.csv?s=' + symbol
    try:
        res = urllib2.urlopen(req_url)
    except urllib2.URLError, e:
        print 'you got an error with the code', e.code
    else:
        body = res.read()
