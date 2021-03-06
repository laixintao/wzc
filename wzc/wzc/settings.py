# -*- coding: utf-8 -*-

SERVER_PORT = 8085

PHANTOMJS_PORT = 12306
TIME_OUT = 50
PHANTOMJS_HOST = 'http://localhost'
PHANTOM_SERVER = '{host}:{port}'.format(host=PHANTOMJS_HOST, port=PHANTOMJS_PORT)

BASE_URL = 'http://python-china.org'

# HTML_PATH = '/Users/laixintao/Documents/wzc/data/'  # absolute path
HTML_PATH = '/Users/laixintao/Documents/wzc/data/'  # absolute path
HOSTS = ['www.python-china.org', 'python-china.org', 'http://www.python-china.org', 'http://python-china.org']

IGNORE_PATH = ['/favicon.ico',]

MIN_UPDATE_TIME = 300
MAX_RETRY = 5

REDIS_SERVER = 'redis://localhost'
MONGO_DB_SERVER = 'mongodb://localhost:27017/'