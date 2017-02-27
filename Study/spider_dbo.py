# coding:utf8
# 数据库操作模块
from DBmodel import mysqldbhand
import md5
import ConfigParser
import time


class dbo(object):

    global mysql
    global table_urls
    global table_contents

    def __init__(self):
        self.mysql = mysqldbhand()
        self.mysql.dbconnect()
        conf = ConfigParser.ConfigParser()
        conf.read('config.conf')
        self.table_urls = conf.get('tables', 'urls')
        self.table_contents = conf.get('tables', 'contents')
        # pass

    def SEARContent(self):
        row = self.mysql.FindAll(
            'fimport', 'autohome', "fid = 235 and autohome !='' ")
        return row

    # 取得 URL 信息
    def url_get_info(self, url):
        url_md5 = md5.md5(url).hexdigest()
        row = self.mysql.FindAll(
            self.table_urls, '*', "url_md5 = '" + url_md5 + "'")
        return row

    # 添加新的 URL
    def url_add_new(self, url):
        url_md5 = md5.md5(url).hexdigest()
        created_time = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        info = {'url': url, 'url_md5': url_md5,
                'created_time': created_time, 'collected': 0}
        res = self.mysql.Save(self.table_urls, info)
        return res

    # def get_url_geted(self, url):
    #     url_md5 = md5.md5(url).hexdigest()
    #     row = self.mysql.FindAll(
    #         self.table_urls, '*', "url_md5 = '" + url_md5 + "'")
    #     print row
        # return row
