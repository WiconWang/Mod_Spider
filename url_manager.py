# coding:utf8
# URL管理器
from DBmodel import mysqldbhand


class UrlManager(object):
    global db
    global tablename

    def __init__(self, table):
        self.new_urls = set()
        self.old_urls = set()
        db = mysqldbhand()
        db.dbconnect()
        self.tablename = table
        project = db.FindAll(table, 'url')
        for m in project:
            self.old_urls.add(m[0])
        # print self.new_urls
        # print self.old_urls

    def add_new_url(self, url):

        # print self.old_urls
        # exit()
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
        print new_url
        print self.new_urls
        print self.old_urls
        # exit
        self.old_urls.add(new_url)
        return new_url
