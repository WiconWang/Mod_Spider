# -*- coding: utf-8 -*-
# 爬取蜻蜓FM财经的几个节目最新一期，并下载下来，提供给mplayer播放
import os
import requests
import time
import redis


class Task(object):
    def __init__(self):
        self.redis = redis.Redis('localhost', 6379)

    def main(self):
        # 选择一系列地址，并查询最新一第是否已经在缓存 中有记录，如果有记录则找下一地址，直到找到一个最新的
        url = [
            'https://www.ximalaya.com/revision/album/getTracksList?albumId=4512647&pageNum=1',
            'https://www.ximalaya.com/revision/album/getTracksList?albumId=9444470&pageNum=1',
        ]
        for i in url:
            audio_url = self.getjson(i)
            if audio_url:
                res_r = self.redis.sismember("audio_xmly_url", audio_url)
                if not res_r:
                    break
        # print(audio_url)
        local_url = self.download(audio_url)
        # print(local_url)
        # 直接播放语音
        os.system('mplayer  -af volume=+15  "%s"' % local_url)

    def getjson(self, url):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/63.0.3239.132 Safari/537.36'}

        # 请求远端服务器并选取JSON
        r = requests.get(url=url, headers=header)
        if r.status_code != 200:
            print('404 Error')
            return False
        trackId = r.json()['data']['tracks'][0]['trackId']
        if not r.json()['data']['tracks'][0]['trackId']:
            return False

        # 取详细情况
        url2 = "http://www.ximalaya.com/tracks/%d.json" % trackId
        r = requests.get(url=url2, headers=header)
        if r.status_code != 200:
            print('404 Error')
            return False
        if not r.json()['play_path']:
            return False
        return r.json()['play_path'], r.json()['album_id'], r.json()['play_path']
        # return "http://%s/%s" % ('od.qingting.fm', r.json()['play_path'])

    # 提取出音频URL启动下载
    def download(self, audio_url):
        timenow = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

        r2 = requests.get(audio_url)
        local_url = "%s/XMLY_%s.m4a" % (os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../Music")), timenow)
        with open(local_url, "wb") as code:
            code.write(r2.content)

        self.redis.sadd("audio_xmly_url", audio_url)
        return local_url


if __name__ == '__main__':
    Task().main()
