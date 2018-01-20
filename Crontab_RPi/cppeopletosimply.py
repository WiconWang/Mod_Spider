# -*- coding: utf-8 -*-
import pymongo



class cpSimply(object):

    global temp

    def __init__(self):
        pass

    def main(self):
        connection = pymongo.MongoClient('127.0.0.1',27017)
        db = connection['crawler_zhaopin']
        mongocomconn = db["zp_com"]
        mongoconn = db["zp"]
        n = 0
        for i in range(0, 100):
            res_db = mongocomconn.find().limit(10).skip(n*10)
            for data in res_db:
                mongoconn.update_many({"com_name": data['com_name']}, {"$set":{'com_person1': data['com_person1'], 'com_person2': data['com_person2']}})
                print(data['com_name'])
            print(n * 10)
            n=n+1
        # pass

if __name__ == '__main__':
    # 初始页面并启动流程
    cpSimply().main()
    pass