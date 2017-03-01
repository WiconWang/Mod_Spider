# coding:utf8
# 入库程序
from DBmodel import mysqldbhand


class HtmlOutputer(object):
    global db
    global tablename

    def __init__(self, table):
        self.datas = []
        self.tablename = table

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        db = mysqldbhand()
        db.dbconnect()
        for data in self.datas:
            res = db.Save(self.tablename, data)
        print res
