# -*- coding: utf-8 -*-

from celery import Celery
from wzc.spider import update_url
from wzc.wzc.settings import BASE_URL

app = Celery('wzc', broker='redis://localhost')


@app.task
def add(x, y):
    return x + y


@app.task
def update(url):
    more_urls = update_url(url)
    for url in more_urls:
        update.delay(BASE_URL+url)
