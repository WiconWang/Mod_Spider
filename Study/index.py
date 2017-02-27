# coding:utf8
# 说明，此逻辑的定位是分离采集 URL 和内容。后期通过定时任务采集 URL 和采集内容
# from DBmodel import mysqldbhand
# import spider_output
import spider_url_manager
import spider_parser
import spider_downloader
import ConfigParser


class SpiderMain(object):

    global start_url
    global conf
    global mod_parser
    global mod_url_manager
    global mod_downloader

    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read('config.conf')
        self.start_url = conf.get('url', 'start_url')
        # 初始化组件
        self.mod_parser = spider_parser.parser()
        self.mod_url_manager = spider_url_manager.url_manager()
        self.mod_downloader = spider_downloader.HtmlDownloader()

    # 跳转一次，启动主逻辑
    def main(self):
        self.work(self.start_url)

    # 主逻辑
    def work(self, url):
        if_need_collect = self.mod_url_manager.need_collect(url)
        if if_need_collect:
            # 下载页面内容
            html_cont = self.mod_downloader.download(url)
            # 解析页面内容
            new_urls, new_data = self.mod_parser.parse(url, html_cont)
            # 检测新 url 并加入待采区
            if new_urls:
                self.mod_url_manager.need_collect(new_urls)
            # 保存新数据

            print new_data
            # res = self.mod_parser._get_new_urls(url)
            print 'OK'
        else:
            print 'PASSED:' + url + ' 不需要采集'
            pass


if __name__ == '__main__':
    # 初始页面并启动流程
    main = SpiderMain()
    main.main()
