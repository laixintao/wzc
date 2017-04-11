# -*- coding: utf-8 -*-
from tornado_fetcher import Fetcher
from wzc.storage import MongodbStorage
from wzc.wzc.settings import HTML_PATH

import re


def extract_urls(html_page):
    ss = html_page.replace(" ", "")
    a_tags = re.findall(r"<a.*?href=.*?<\/a>", ss, re.I)
    urls = []
    for i in a_tags:
        href = re.findall(r'href=".*?"',i)[0]
        urls.append(href[6:-1])
    return urls


def update_url(url):
    '''
    :param url:
    :return: more urls
    '''
    fetcher = Fetcher(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        # user agent
        pool_size=10,  # max httpclient num
        async=False
    )
    res = fetcher.phantomjs_fetch(url)
    content = res['content']
    mongo = MongodbStorage()
    filename = mongo.save(res)
    with open('{}{}.html'.format(HTML_PATH, filename), 'w') as f:
        f.write(content.encode('utf-8'))
    more_urls = extract_urls(content)
    return more_urls


if __name__ == '__main__':
    update_url('http://www.python-china.org')
