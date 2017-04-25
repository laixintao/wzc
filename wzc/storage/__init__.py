# -*- coding: utf-8 -*-

import pymongo
import hashlib
from urlparse import urlparse

conn = pymongo.MongoClient()
page_table = conn['wzc']['page']
fail_page = conn['wzc']['fail_page']

class MongodbStorage(object):
    def __init__(self):
        self.page_info = {}
        self.page = page_table
        self.fail_page = fail_page

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
        del result['content']
        if result['status'] == 'success':
            target_db = self.page
        else:
            target_db = self.fail_page
        target_db.update({'path': result['path']},
                         {'$set': result}, upsert=True)
        return hash_md5


if __name__ == '__main__':
    db = MongodbStorage()
    db.save({'nihao': '你好'})
