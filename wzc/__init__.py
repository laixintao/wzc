# -*- coding: utf-8 -*-
from spider.tornado_fetcher import Fetcher

if __name__ == '__main__':
    fetcher = Fetcher(
        user_agent='phantomjs',  # user agent
        phantomjs_proxy='http://localhost:12306',  # phantomjs url
        pool_size=10,  # max httpclient num
        async=False
    )
    content = fetcher.phantomjs_fetch('http://python-china.org/')
    print content.keys()
    print content['content']
    with open('download.html', 'w') as f:
        f.write(content['content'].encode('utf-8'))