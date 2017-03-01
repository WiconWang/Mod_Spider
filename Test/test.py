# -*- coding:utf-8 -*-

import urllib2
# import cookielib
import bs4

# 取得页面内容
site = "http://www.huiye360.com"
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

req = urllib2.Request(site, headers=hdr)

try:
    page = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.fp.read()

content = page.read()

# 取出所有连接
soup = bs4.BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
links = soup.find_all('a')
for link in links:
    print link.name, link['href'], link.get_text()
