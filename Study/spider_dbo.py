# coding:utf8
# 数据库操作模块
from DBmodel import mysqldbhand
import md5


class spider_dbo(object):

    global mysql

    def __init__(self):
        self.mysql = mysqldbhand()
        self.mysql.dbconnect()
        pass

    def SaveContent(self):
        print('ccc')
        row = self.mysql.FindAll(
            'fimport', 'autohome', "fid = 235 and autohome !='' ")
        return row

    def get_url_info(self, url):
        url_md5 = md5.md5(url).hexdigest()
        row = self.mysql.FindAll(
            'bbs_list', '*', "url_md5 = '" + url_md5 + "'")
        return row
