# -*- coding: utf-8 -*-

import logging
import copy
import json
import time

import tornado.httpclient
from tornado.curl_httpclient import CurlAsyncHTTPClient
import tornado.ioloop

from wzc.wzc.settings import PHANTOM_SERVER, TIME_OUT, MIN_UPDATE_TIME
from wzc.storage import page_table

logger = logging.getLogger(__name__)


def text(obj, encoding='utf-8'):
    if isinstance(obj, unicode):
        return obj.encode(encoding)
    return obj


def unicode_obj(obj, encoding='utf-8'):
    if isinstance(obj, str):
        return obj.decode(encoding)
    return obj


class Fetcher(object):
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
        if self.async:
            self.http_client = CurlAsyncHTTPClient(max_clients=pool_size, io_loop=tornado.ioloop.IOLoop())
        else:
            self.http_client = tornado.httpclient.HTTPClient(max_clients=pool_size)

    @staticmethod
    def parse_option(default_options, url, user_agent, **kwargs):
        fetch = copy.deepcopy(default_options)
        fetch['url'] = url
        fetch['headers']['User-Agent'] = user_agent
        js_script = kwargs.get('js_script')
        if js_script:
            fetch['js_script'] = js_script
            fetch['js_run_at'] = kwargs.get('js_run_at', 'document-end')
        fetch['load_images'] = kwargs.get('load_images', False)
        return fetch

    def check_need_update(self, url):
        page_info = page_table.find_one({'path': url})
        if not page_info:
            return True
        now_time = time.time()
        if now_time - page_info['last_update'] < MIN_UPDATE_TIME:
            logger.debug('trying to update url {}, but not out {}'.format(url, MIN_UPDATE_TIME))
            return False
        return True

    def phantomjs_fetch(self, url, **kwargs):
        if not self.check_need_update(url):
            return
        start_time = time.time()
        fetch = self.parse_option(self.default_options, url, user_agent=self.user_agent, **kwargs)
        request_conf = {
            'follow_redirects': False
        }
        if 'timeout' in fetch:
            request_conf['connect_timeout'] = fetch['timeout']
            request_conf['request_timeout'] = fetch['timeout'] + 1

        def handle_response(response):
            """handle response, this function must be called."""
            if not response.body:
                return handle_error(Exception('no response from phantomjs'))
            try:
                result = json.loads(text(response.body))
                if response.error:
                    result['error'] = text(response.error)
            except Exception as e:
                return handle_error(e)

            if result.get('status_code', 200):
                logging.info('[%d] %s %.2fs', result['status_code'], url, result['time'])
            else:
                logging.error('[%d] %s, %r %.2fs', result['status_code'],
                              url, result['content'], result['time'])
            result['status'] = 'success'
            return result

        def handle_error(error):
            result = {
                'status_code': getattr(error, 'code', 599),
                'error': unicode_obj(error),
                'content': '',
                'time': time.time() - start_time,
                'orig_url': url,
                'url': url,
                'status': 'error'
            }
            logging.error('[%d] %s, %r %.2fs',
                          result['status_code'], url, error, result['time'])
            return result
        try:
            request = tornado.httpclient.HTTPRequest(
                url='%s' % self.phantomjs_proxy, method='POST',
                body=json.dumps(fetch), **request_conf)
            if self.async:
                self.http_client.fetch(request, handle_response)
            else:
                return handle_response(self.http_client.fetch(request))
        except tornado.httpclient.HTTPError as e:
            if e.response:
                return handle_response(e.response)
            else:
                return handle_error(e)
        except Exception as e:
            return handle_error(e)
