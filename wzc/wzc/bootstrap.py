# -*- coding: utf-8 -*-
import sys
from os.path import abspath, join, dirname

from wzc.spider.tornado_fetcher import Fetcher
from settings import PHANTOM_SERVER, BASE_URL


def start_job():
    fetcher = Fetcher(
        user_agent='phantomjs',  # user agent
        phantomjs_proxy=PHANTOM_SERVER,  # phantomjs url
        pool_size=10,  # max httpclient num
        async=False
    )
    content = fetcher.phantomjs_fetch(BASE_URL)
    print content.keys()
    print content['content']
    with open('download.html', 'w') as f:
        f.write(content['content'].encode('utf-8'))


if __name__ == '__main__':
    start_job()
