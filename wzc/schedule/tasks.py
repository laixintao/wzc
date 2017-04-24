# -*- coding: utf-8 -*-
# pylint: disable=C0103

"""
managing spider tasks.
"""

from celery import Celery
from wzc.spider import update_url
from wzc.wzc.settings import BASE_URL

wzc_spider = Celery('wzc', broker='redis://localhost')

@wzc_spider.task
def update(url):
    """url update task"""
    more_urls = update_url(url)
    if more_urls is None:
        return
    for url in more_urls:
        update.delay(BASE_URL+url)
