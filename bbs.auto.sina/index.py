# coding:utf8
# 说明，此逻辑的定位是分离采集 URL 和内容。后期通过定时任务采集 URL 和采集内容
# from DBmodel import mysqldbhand
# import spider_output
import spider_url_manager
import spider_parser
import spider_downloader
import spider_dbo
import ConfigParser
import time


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
        self.mod_dbo = spider_dbo.dbo()

    # 跳转一次，启动主逻辑
    def main(self):
        self.work(self.start_url)
        self.loop_work()

    # 从数据库中取到一条未采集的 URL 并进行采集
    def loop_work(self):
        url_need_collect = self.mod_dbo.url_get_need_collect()
        if url_need_collect and url_need_collect[0]['url']:
            # 取一下缓存列表，如果已经采集则同步更新到 db，未采集则进行采集
            url = url_need_collect[0]['url']
            print url
            if self.mod_url_manager.url_not_collected(url):
                self.work(url)
                time.sleep(1)
            else:
                self.mod_dbo.url_up_collected(url)
            # 递归下一条记录
            self.loop_work()
            return True
        else:
            return False

    # 主逻辑
    def work(self, url):
        # 检测是否为需要采集的项目
        if_need_collect = self.mod_url_manager.need_collect(url)
        if if_need_collect:
            # 下载页面内容
            html_cont = self.mod_downloader.download(url)
            # 解析页面内容
            new_urls, new_data = self.mod_parser.parse(url, html_cont)
            # 检测新 url 并加入待采区
            if new_urls:
                for new_single_url in new_urls:
                    self.mod_url_manager.need_collect(new_single_url)
            # 保存新数据到内容区
            if new_data:
                # result =
                self.mod_dbo.content_add_new(new_data)

            # 把本条 URL 更新为已采集
            self.mod_dbo.url_up_collected(url)
            # 把本条添加进已经采集缓存
            self.mod_url_manager.collected_list(url)
        else:
            print 'PASSED:' + url + ' 不需要采集'
        # 返回本条已经采集完成
        return True


if __name__ == '__main__':
    # 初始页面并启动流程
    main = SpiderMain()
    main.main()
