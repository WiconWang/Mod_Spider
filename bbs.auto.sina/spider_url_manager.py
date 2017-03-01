# coding:utf8
# 任务管理器
import spider_dbo
import md5
# from DBmodel import mysqldbhand


class url_manager(object):
    global dbo
    global finished_urls

    def __init__(self):
        # 初始化组件
        self.dbo = spider_dbo.dbo()
        self.finished_urls = set()
        # 加载已经采集列表 防止重复采集
        urls_collected = self.dbo.url_get_collected()
        for i in range(len(urls_collected)):
            self.finished_urls.add(urls_collected[i]['url_md5'])

    # 此URL是否需要后续采集,如果是新 url 则加入待采区
    def need_collect(self, url):
        url_info = self.dbo.url_get_info(url)
        if url_info:
            if url_info[0]['collected'] == 1:
                return False
            else:
                return True
        else:
            # 保存页面
            self.dbo.url_add_new(url)
            return True

    # 缓存当前已经采集的 URL 列表的 md5值
    def collected_list(self, url=''):
        if url:
            url_md5 = md5.md5(url).hexdigest()
            self.finished_urls.add(url_md5)
        return self.finished_urls

    # 检索是否已采集
    def url_not_collected(self, url):
        # print self.finished_urls
        url_md5 = md5.md5(url).hexdigest()
        if url_md5 not in self.finished_urls:
            return True
        else:
            return False
