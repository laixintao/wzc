# -*- coding: utf-8 -*-
from tornado_fetcher import Fetcher
from wzc.storage import MongodbStorage
from wzc.wzc.settings import HTML_PATH


def update_url(url):
    '''
    :param url:
    :return: res [u'cookies', u'url', u'orig_url', u'time', u'content', u'headers', u'status_code', u'js_script_result']
    '''
    fetcher = Fetcher(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',  # user agent
        pool_size=10,  # max httpclient num
        async=False
    )
    res = fetcher.phantomjs_fetch(url)
    mongo = MongodbStorage()
    filename = mongo.save(res)
    with open('{}{}.html'.format(HTML_PATH, filename), 'w') as f:
        f.write(res['content'].encode('utf-8'))


if __name__ == '__main__':
    update_url('http://www.python-china.org')
