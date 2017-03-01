# coding:utf8
# URL管理器
from DBmodel import mysqldbhand
import ConfigParser


class UrlManager(object):
    global db
    global tablename
    global root_url

    def __init__(self, table):
        self.new_urls = set()
        self.old_urls = set()
        cf = ConfigParser.ConfigParser()
        cf.read("config.conf")
        self.root_url = '%s' % cf.get("start", "root_url")
        # 找出DB中检出的记录，并做为已采集记录进行流程排除
        db = mysqldbhand()
        db.dbconnect()
        self.tablename = table
        project = db.FindAll(table, 'url')
        for m in project:
            self.old_urls.add(m[0])
        # print self.new_urls
        # print self.old_urls

    def add_new_url(self, url):
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def has_new_url(self):
        return len(self.new_urls) != 0

    def get_new_url(self):
        new_url = self.new_urls.pop()
        # print new_url
        # print self.new_urls
        # print self.old_urls
        # exit
        self.old_urls.add(new_url)
        return new_url
