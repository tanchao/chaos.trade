#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'tanchao'

from flask import Flask
from utils import chaos_trade

app = Flask(__name__)

@app.route('/ct')
def trade():
    # 0. prepare data
    # 1. query database
    # 2. selector rules
    # 3. save result to db
    pass

@app.route('/chaos')
@app.route('/chaos/<market>')
@app.route('/chaos/<market>/<rate>')
def chaos(market='all', rate=0.9):
    selected = chaos_trade.chaos(market, rate)
    res = ''
    for x in selected:
        res += str(x) + ' : ' + str(selected[x]) + '</br>'
    return res

@app.route('/')
def hello_world():
    return 'Hello Flask!'


if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)
