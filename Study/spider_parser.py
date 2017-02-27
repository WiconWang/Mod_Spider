# coding:utf8
# 页面解析工具

from bs4 import BeautifulSoup
import re
import urlparse


class parser(object):

    global temp

    # 采集相关 URL
    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # css 方式
        # links = soup.find_all("a", class_="xst")
        # 正则方式
        links = soup.find_all("a", href=re.compile("^b"))
        # links = soup.find_all('a', href=re.compile(
            # r"soup.find( \'table\', id=\"threadlisttableid\").find(\"a\")"))
        print links
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        print new_urls
        # return new_urls

    # 采集相关内容
    def _get_new_data(self, page_url, soup):
        res_data = {}
        temp_data = ''

        # url
        res_data['url'] = page_url

        # 其它等收集的字段
        for field in self.project_field:
            temp_data = eval(field[4])
            res_data["%s" % (field[2])] = temp_data.get_text()
        print res_data
        # return res_data

    # 解析主逻辑
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='urf-8')
        new_urls = self._get_new_urls(page_url, soup)
        # new_data = self._get_new_data(page_url, soup)
        new_data = 'new_data'
        return new_urls, new_data
