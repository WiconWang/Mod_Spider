# -*- coding: utf-8 -*-
# 爬取蜻蜓FM财经的几个节目最新一期，并下载下来，提供给mplayer播放
import configparser
import os
import requests
import time
import redis


class Task(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.readfp(open(os.path.join(os.path.dirname(__file__), "config.ini")))
        self.host = config.get("LOCAL_REDIS", "Host")
        self.port = config.get("LOCAL_REDIS", "Port")
        self.redis_key = config.get("QING_TING", "Redis_key")
        self.file_staff = config.get("QING_TING", "File_staff")
        self.redis = redis.Redis(self.host, self.port)

    def main(self):
        # 选择一系列地址，并查询最新一第是否已经在缓存 中有记录，如果有记录则找下一地址，直到找到一个最新的
        url = [
            'http://i.qingting.fm/wapi/channels/74000/programs/page/1',
            'http://i.qingting.fm/wapi/channels/108208/programs/page/1',
            'http://i.qingting.fm/wapi/channels/141268/programs/page/1'
        ]
        for i in url:
            audio_url = self.getjson(i)
            if audio_url:
                res_r = self.redis.sismember(self.redis_key, audio_url)
                if not res_r:
                    break

        local_url = self.download(audio_url)
        print(local_url)
        # 直接播放语音
        os.system('mplayer  -af volume=+15  "%s"' % local_url)

    def getjson(self, url):

        # 请求远端服务器并选取JSON
        r = requests.get(url=url)
        if r.status_code != 200:
            print('404 Error')
            return False
        if not r.json()['data'][0]['file_path']:
            return False
        return "http://%s/%s" % ('od.qingting.fm', r.json()['data'][0]['file_path'])

    # 提取出音频URL启动下载
    def download(self, audio_url):
        timenow = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

        r2 = requests.get(audio_url)
        local_url = "%s/%s_%s.m4a" % (os.path.abspath(
            os.path.join(os.path.dirname(__file__), "./Audio")), self.file_staff, timenow)
        with open(local_url, "wb") as code:
            code.write(r2.content)

        self.redis.sadd(self.redis_key, audio_url)
        return local_url


if __name__ == '__main__':
    Task().main()
