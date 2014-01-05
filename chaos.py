# -*- coding: utf-8 -*-
# (c) tanchao <chaos.tc@gmail.com>

import json

import web
import config

import controllers.stock

urls = (
    '/', 						'index',
    '/stock/ema5/(.+)', 		'ema5',
    '/stock/(.+)', 				'stock',
    '/test',					'test',
)

# render configuration
template_globals = {
    'datestr': web.datestr
}

view = web.template.render('views', base='base', globals=template_globals)
jd = [{'user': 'tc'}]


def get_stock_file(stock_code_):
    return config.ROOT + 'static/docs/data/' + stock_code_ + '.csv'


class test:

    def GET(self):
        d_ = {'data': [[0, 0], [1, 1], [2, 2], [3, 4]]}
        return view.stocks(json.dumps(d_))


class stock:

    def GET(self, stock_code_):
        stock_file_ = get_stock_file(stock_code_)
        d_ = controllers.stock.get_stock_from_csv(stock_file_)
        jd.append(d_)
        return view.stock(json.dumps(jd))


class ema5:

    def GET(self, stock_code_):
        stock_file_ = get_stock_file(stock_code_)
        d_ = controllers.stock.get_ema5_from_csv(stock_file_)
        return json.dumps(d_)


class index:

    def GET(self):
        ''' Index Page '''
        return view.index()  # render.index()

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()
