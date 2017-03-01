# coding:utf8
# 下载器

import urllib2


class HtmlDownloader(object):

    def download(self, url):
        if url is None:
            return None

        response = urllib2.urlopen(url)

        if response.getcode() != 200:
            return None
        # 设置一下编码，防止 keywords 等因书写不规范无法采出的问题
        # 注意这种方法也有很多问题，尤其是英文站
        charset = response.headers['Content-Type'].lower().split("charset=")[1]
        return response.read().decode(charset, "ignore").encode("utf-8", 'ignore')
