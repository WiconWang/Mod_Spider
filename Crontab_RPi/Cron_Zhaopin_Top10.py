# -*- coding: utf-8 -*-
# 取出Mongodb中前几个招聘数据

import redis
import pymongo


class Task(object):
    def __init__(self):
        pass
        # self.redis = redis.Redis('localhost', 6379)

    def main(self):
        connection = pymongo.MongoClient('127.0.0.1', 27017)
        db = connection['crawler_zhaopin']
        mongo_conn = db["zp"]
        res_db = mongo_conn.find({'post_salary2': {'$gte': 1200}, 'ptype': 'sj2041', 'com_person2': {'$gte': 400}}).limit(100).sort("post_salary2", pymongo.DESCENDING)
        for data in res_db:
            print(data['com_name'])







if __name__ == '__main__':
    Task().main()
