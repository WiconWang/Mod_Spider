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

    def url_get_need_collect(self):
        row = self.mysql.FindAll(
            self.table_urls, 'url', " collected = '0' ", " id asc ", " 1 ")
        return row

    def url_get_collected(self):
        row = self.mysql.FindAll(
            self.table_urls, 'url_md5', " collected = '1' ", " id asc ", " 10000 ")
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

    def url_up_collected(self, url):
        url_md5 = md5.md5(url).hexdigest()
        info = {'collected': 1}
        res = self.mysql.Save(self.table_urls, info, {'url_md5': url_md5})
        if res:
            return True
        else:
            return False

    # 取得 URL 信息
    def content_get_info(self, url):
        url_md5 = md5.md5(url).hexdigest()
        row = self.mysql.FindAll(
            self.table_contents, '*', "url_md5 = '" + url_md5 + "'")
        return row

    def content_add_new(self, data):
        url_md5 = md5.md5(data['url']).hexdigest()
        content_info = self.content_get_info(data['url'])
        if content_info:
            return False
        else:
            created_time = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            info = {'url': data['url'], 'url_md5': url_md5,
                    'created_time': created_time, 'title': data['title'],
                    'descript': data['descript'],
                    'keywords': data['keywords'],
                    'content': data['content']}
            res = self.mysql.Save(self.table_contents, info)
            return res
