# -*- coding: utf-8 -*-
# pylint: disable=C0103

"""
managing spider tasks.
"""
import logging

from celery import Celery
from wzc.spider import update_url
from wzc.wzc.settings import BASE_URL, MAX_RETRY

wzc_spider = Celery('wzc', broker='redis://localhost')
logger = logging.getLogger(__name__)

@wzc_spider.task
def update(url, retry_left=MAX_RETRY):
    """url update task"""
    if retry_left < 0:
        logger.error("no retry times left when trying to update {}".format(url))
        return
    more_urls = update_url(url)
    if more_urls:
        for url in more_urls:
            update.delay(BASE_URL+url)
    else:
        retry_left -= 1
        update.delay(url, retry_left)