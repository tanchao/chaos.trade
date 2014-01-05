# -*- coding: utf-8 -*-
# (c) tanchao <chaos.tc@gmail.com>

import os

import web

''' application root '''
ROOT = os.getcwd() + os.path.sep

''' sina stock data api
eg: http://hq.sinajs.cn/list=sh600389
var hq_str_sh600389="stock name,15.31,15.74,15.68,16.02,15.16,15.68,15.69,4044916,62900903,3350,15.68,9700,15.60,1000,15.57,2384,15.56,2100,15.54,13100,15.69,73100,15.70,1000,15.72,4000,15.74,14200,15.75,2013-01-11,14:14:24,00";
http://hq.sinajs.cn/list=sh600000,sh600004
http://hq.sinajs.cn/list=s_sh000001
http://hq.sinajs.cn/list=s_sz399001
'''

''' tencent stock data api
http://qt.gtimg.cn/r=0.8409869808238q=s_sz000559,s_sz000913,s_sz002048,s_sz002085,s_sz002126,s_sz002284,s_sz002434,s_sz002472,s_sz002488
'''

''' 163 stock data api
http://api.money.126.net/data/feed/1002151,0600036,0600016,0600000,0601398,0600031,1000002,1000858,0601166,0601318,0600019,0601857,1000078,1002024,0600028,money.api?callback=_ntes_quote_callback13451765
'''

''' yahoo stock data api
http://table.finance.yahoo.com/table.csv?s=000157.sz&d=6&e=22&f=2013&g=d&a=11&b=06&c=2013&ignore=.csv
'''

''' GOOGLE FINANCE HK
https://www.google.com.hk/finance?chdnp=1&chdd=1&chds=1&chdv=1&chvs=maximized&chdeh=0&chfdeh=0&chdet=1386745200000&chddm=55912&chls=IntervalBasedLine&q=SHE:000157&&fct=big&ei=a_anUoHSOI7p0QH1JA&gl=cn
'''

# Real Time data define as sina
RT_SD_URL = 'http://hq.sinajs.cn/list='

# History stock data define as yahoo
HIS_SD_URL = 'http://table.finance.yahoo.com/table.csv?s='

# development mode
web.config.debug = True

# db configuration
db = web.database(dbn='postgres', user='postgres', pw='tc', db='chaos')
