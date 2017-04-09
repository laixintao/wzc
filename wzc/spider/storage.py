# -*- coding: utf-8 -*-

import pymongo


class MongodbStorage(object):
    def __init__(self):
        self.page_info = {}
        conn = pymongo.MongoClient()
        self.db = conn['hello']['world']

    def save(self, result):
        '''
        Saving html to file, and other infomation to mongo.
        use a md5 code stored in mongo to located file.
        :param result: key response
        :return:
        '''
        html = result.get('content')
        
        self.db.insert(result)


if __name__ == '__main__':
    db = MongodbStorage()
    db.save({'nihao':'你好'})
