#!/bin/bash

# configured this socket to bind nginx: chaos_nginx.conf
# https://uwsgi-docs.readthedocs.org/en/latest/Nginx.html?highlight=nginx

# run this command to call app via wsgi
# https://uwsgi-docs.readthedocs.org/en/latest/WSGIquickstart.html#installing-uwsgi-with-python-support
uwsgi --socket 127.0.0.1:9527 --wsgi-file chaos.py --callable app --master --processes 4 --threads 2 --logto /tmp/uwsgi.log
