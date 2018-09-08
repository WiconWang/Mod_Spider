# -*- coding: utf-8 -*-
# 取出Mongodb中前几个招聘数据
import time

import configparser
from datetime import datetime, timedelta

import redis
import pymongo
import json
import os
from collections import defaultdict


class Task(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.readfp(open(os.path.join(os.path.dirname(__file__), "config.ini")))
        self.host = config.get("LOCAL_MONGO", "host")
        self.port = config.get("LOCAL_MONGO", "port")
        # pass
        # self.redis = redis.Redis('localhost', 6379)

    def main(self):
        connection = pymongo.MongoClient(self.host, self.port)
        db = connection['crawler_zhaopin']
        mongo_conn = db["zp"]
        timestart =datetime.now() - timedelta(days=60)
        # print(timestart)
        # 12000以上，60天内，sj2041类型，400人以上
        res_db = mongo_conn.find({'post_salary2': {'$gte': 12000}, 'post_date': {'$gte': timestart}, 'ptype': 'sj2041', 'com_person2': {'$gte': 400}, 'com_name': {'$regex': '^(?!.*(达内|传智)).*$'}}).limit(100).sort("post_salary2", pymongo.DESCENDING)
        arr = dict()
        for data in res_db:
            del data['_id']
            del data['url_md5']
            del data['post_desc']
            del data['collect_time']
            del data['location']
            data['post_time'] = data['post_date'].strftime('%Y-%m-%d %H:%M:%S')
            del data['post_date']
            aa = dict()
            aa['url_md5'] = dict()
            aa['url_md5'] = data
            print(aa)
            # dict(d1.items() + data.items())
            # arr.update(data)
            # arr.setdefault()
              # arr[data['url_md5']]=dict()
            # arr[data['url_md5']].update(data)

            # arr = dict.fromkeys(data['city'])
            # arr = dict(data['city']=data)
            # arr[data['city']].append(data)
        # print(arr)
        # json.dump(arr, open('result.json', 'w'))








if __name__ == '__main__':
    Task().main()
