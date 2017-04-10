# -*- coding: utf-8 -*-

import pymongo
import hashlib


class MongodbStorage(object):
    def __init__(self):
        self.page_info = {}
        conn = pymongo.MongoClient()
        self.db = conn['wzc']['page']

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
        self.db.insert(result) #TODO update
        return hash_md5


if __name__ == '__main__':
    db = MongodbStorage()
    db.save({'nihao':'你好'})
