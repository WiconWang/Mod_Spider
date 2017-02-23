# coding:utf8
# from DBmodel import mysqldbhand
# import spider_output
import spider_url_manager
import ConfigParser


class SpiderMain(object):

    global start_url
    global conf

    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read('config.conf')
        self.start_url = conf.get('url', 'start_url')

    def main(self):
        url_manager = spider_url_manager.spider_url_manager()
        url_list = url_manager.start_url(self.start_url)
        print(url_list)

if __name__ == '__main__':
    # 初始页面并启动流程
    main = SpiderMain()
    main.main()
