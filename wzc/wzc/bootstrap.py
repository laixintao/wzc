# -*- coding: utf-8 -*-


from wzc.spider.tornado_fetcher import Fetcher
from settings import PHANTOM_SERVER, BASE_URL
from wzc.schedule import tasks

def start_job():
    tasks.update.delay(BASE_URL)


if __name__ == '__main__':
    start_job()
