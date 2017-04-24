# -*- coding: utf-8 -*-
"""
phantomjs fetcher
"""
from __future__ import unicode_literals, print_function

import copy
import json
import time

import tornado.httpclient
import tornado.ioloop

from wzc.wzc.settings import PHANTOM_SERVER, TIME_OUT



class Fetcher(object):
    """ pahntomjs fetcher """
    default_options = {
        'method': 'GET',
        'headers': {},
        'allow_redirects': True,
        'use_gzip': True,
        'timeout': TIME_OUT,
    }

    def __init__(self, phantomjs_proxy=PHANTOM_SERVER, user_agent='', pool_size=100, async=False):
        self.phantomjs_proxy = phantomjs_proxy
        self.user_agent = user_agent
        self.async = async
        self.url = ""
        # TODO support async
        self.http_client = tornado.httpclient.HTTPClient(max_clients=pool_size)

    @staticmethod
    def parse_option(default_options, url, user_agent, **kwargs):
        """ parse_option """
        fetch = copy.deepcopy(default_options)
        fetch['url'] = url
        fetch['headers']['User-Agent'] = user_agent
        js_script = kwargs.get('js_script')
        if js_script:
            fetch['js_script'] = js_script
            fetch['js_run_at'] = kwargs.get('js_run_at', 'document-end')
        fetch['load_images'] = kwargs.get('load_images', False)
        return fetch

    def phantomjs_fetch(self, url, **kwargs):
        """ main fetcher method """
        self.url = url
        start_time = time.time()
        fetch_resp = {'start_time': start_time}
        fetch = self.parse_option(self.default_options, url, user_agent=self.user_agent, **kwargs)
        request_conf = {
            'follow_redirects': False
        }
        if 'timeout' in fetch:
            request_conf['connect_timeout'] = fetch['timeout']
            request_conf['request_timeout'] = fetch['timeout'] + 1
        try:
            request = tornado.httpclient.HTTPRequest(url=self.phantomjs_proxy, method='POST',
                                                     body=json.dumps(fetch), **request_conf)
            phantomjs_response = self.http_client.fetch(request)
            result = json.loads(phantomjs_response.body)
            result['status'] = 'success'
        except Exception as error_info:
            result = {'status_code': getattr(error_info, 'code', 599),
                      'error_info': str(error_info),
                      'content': '',
                      'time': time.time() - start_time,
                      'orig_url': url,
                      'url': url,
                      'status': 'error',
                     }
        finally:
            fetch_resp = result.update(fetch_resp)
        return fetch_resp

if __name__ == '__main__':
    test_url = "http://python-china.org/t/1257"
    test_fetcher = Fetcher(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        # user agent
        pool_size=10,  # max httpclient num
        async=False
    )
    test_res = test_fetcher.phantomjs_fetch(test_url)
    print(test_res)
