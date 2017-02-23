# coding:utf8
# 任务管理器
import spider_dbo
# from DBmodel import mysqldbhand


class spider_url_manager(object):

    # global mysql

    # def __init__(self):
    #     self.mysql = mysqldbhand()
    #     self.mysql.dbconnect()
    #     pass

    def start_url(self, url):
        record = self.is_exist_url(url)
        print(record)
        # row = self.mysql.FindAll(
        #     'fimport', 'autohome', "fid = 235 and autohome !='' ")
        # return row
        pass

    def add_new_url(self, url):
        pass

    def is_exist_url(self, url):
        dbo = spider_dbo.spider_dbo()
        url_info = dbo.get_url_info(url)
        if url_info:
            print('已经存在这个URL了')
        else:
            print('not is')
