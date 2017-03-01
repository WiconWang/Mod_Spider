# coding:utf8
# 解析器
from bs4 import BeautifulSoup
import re
import urlparse


class HtmlParser(object):
    global db
    global project
    global project_field

    def __init__(self, table, project, project_field):
        self.datas = []
        self.project = project[0]
        self.project_field = project_field

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r"%s" % (self.project[5])))

        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}
        temp_data = ''

        # url
        res_data['url'] = page_url

        # 其它等收集的字段
        for field in self.project_field:
            temp_data = eval(field[4])
            res_data["%s" % (field[2])] = temp_data.get_text()

        return res_data

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='urf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)

        return new_urls, new_data
