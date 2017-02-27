# coding:utf8
# 任务管理器
import spider_dbo
# from DBmodel import mysqldbhand


class url_manager(object):
    global dbo

    def __init__(self):
        # 初始化组件
        self.dbo = spider_dbo.dbo()

    # def __init__(self):
    #     self.mysql = mysqldbhand()
    #     self.mysql.dbconnect()
    #     pass

    # def start_url(self, url):
    #     record = self.is_exist_url(url)
    #     print(record)
    #     # row = self.mysql.FindAll(
    #     #     'fimport', 'autohome', "fid = 235 and autohome !='' ")
    #     # return row
    #     pass

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
