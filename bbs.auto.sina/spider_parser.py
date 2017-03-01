# coding:utf8
# 页面解析工具

from bs4 import BeautifulSoup
import re
import urlparse


class parser(object):

    global temp

    # 采集相关 URL
    def _get_new_urls(self, page_url, soup):
        # 定义set 集合进行去重
        new_urls = set()
        # css 方式
        # links = soup.find_all("a", class_="xst")
        # 正则方式
        links = soup.find_all("a", href=re.compile(".*(thread|forum).*html"))
        # links = soup.find_all('a', href=re.compile(
        # r"soup.find( \'table\', id=\"threadlisttableid\").find(\"a\")"))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        # print new_urls
        return new_urls

    # 采集相关内容
    def _get_new_data(self, page_url, soup):
        # 定义字段
        content_temp = soup.find("td", class_="t_f")
        if not content_temp:
            return False
        content = content_temp.contents
        title = soup.title.contents
        descript = soup.find(attrs={"name": "description"})['content']
        keywords = soup.find(attrs={"name": "keywords"})['content']
        # content =  soup.find_all("td", class_="t_f")[0].contents
        # 'content': soup.select("td.t_f"),
        # .get_text(),可以只取内容，清除其它所有
        # .contents 取到子元素集
        project_field = {'url': page_url,
                         'title': ''.join(title),
                         'descript': descript,
                         'keywords': keywords,
                         'content': "".join(map(str, content)),
                         }
        if project_field['title'] == '' or project_field['content'] == '':
            return False
        else:
            return project_field
        # for k, v in project_field.iteritems():
        #     print "Key %s, V %s" % (k, v)

    # 解析主逻辑
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='urf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data
