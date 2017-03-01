# coding:utf8
# 页面初始 和controller

from DBmodel import mysqldbhand
import url_manager
import html_downloader
import html_parser
import html_outputer
import ConfigParser


class SpiderMain(object):

    global temp
    global db
    global projectid
    global tablename
    global number

    def __init__(self):
        # 初始化配置
        cf = ConfigParser.ConfigParser()
        cf.read("config.conf")
        self.projectid = '%s' % cf.get("start", "project_id")
        self.root_url = '%s' % cf.get("start", "root_url")
        self.number = '%s' % cf.get("start", "number")

        # 启动表连接
        db = mysqldbhand()
        db.dbconnect()
        db.init_tables(self.projectid)
        project = db.FindAll('project', '*', where='id= %s' % (self.projectid))
        project_field = db.FindAll(
            'project_field', '*', where='pid= %s' % (self.projectid))
        self.tablename = project[0][2] + '_content'
        # 加载URL管理器
        self.urls = url_manager.UrlManager(self.tablename)
        # 加载下载器
        self.downloader = html_downloader.HtmlDownloader()
        # 加载页面解析器
        self.parse = html_parser.HtmlParser(
            self.tablename, project, project_field)
        # 加载入库程序
        self.outputer = html_outputer.HtmlOutputer(self.tablename)

    def main(self):
        count = 1
        self.urls.add_new_url(self.root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print 'craw %d : %s' % (count, new_url)
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parse.parse(new_url, html_cont)
                # print new_url
                self.urls.add_new_urls(new_urls)
                # 保存时排除掉起始页
                if new_url != self.root_url:
                    self.outputer.collect_data(new_data)

                if count == int(self.number):
                    break

                count = count + 1
            except:
                print "Craw failed"

        self.outputer.output_html()

if __name__ == '__main__':
    # 初始页面并启动流程
    obj_spider = SpiderMain()
    obj_spider.main()
