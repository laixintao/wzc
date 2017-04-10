# -*- coding: utf-8 -*-

import pymongo
import hashlib
from urlparse import urlparse

conn = pymongo.MongoClient()
page_table = conn['wzc']['page']

class MongodbStorage(object):
    def __init__(self):
        self.page_info = {}
        self.db = page_table

    def save(self, result):
        '''
        Saving html to file, and other infomation to mongo.
        use a md5 code stored in mongo to located file.
        :param result: key response
        :return: md5 string
        '''
        html = result.get('content')
        hash_md5 = hashlib.md5(html.encode('utf-8')).hexdigest()
        result['md5'] = hash_md5
        url_scheme = urlparse(result.get('url'))
        result['netloc'] = url_scheme.netloc
        result['path'] = url_scheme.path
        self.db.insert(result) #TODO update
        return hash_md5


if __name__ == '__main__':
    db = MongodbStorage()
    db.save({'nihao':'你好'})
