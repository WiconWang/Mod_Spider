# coding:utf8
# 调度器
import url_manager
import html_downloader
import html_parser
import html_outputer


class SpiderMain(object):
    def __init__(self):
        # 加载URL管理器
        self.urls = url_manager.UrlManager()
        # 加载下载器
        self.downloader = html_downloader.HtmlDownloader()
        # 加载页面解析器
        self.parse = html_parser.HtmlParser()
        # 加载入库程序
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()
                print 'craw %d : %s' % (count, new_url)
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parse.parse(new_url, html_cont)
                # print new_urls
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)

                if count == 3:
                    break

                count = count + 1
            except:
                print "Craw failed"

        self.outputer.output_html()


if __name__ == '__main__':
    # 初始页面并启动流程
    root_url = "http://baike.baidu.com/subview/99/5828265.htm"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
