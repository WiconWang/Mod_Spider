# -*- coding: utf-8 -*-
# 读取指定目录文件名，并播放
import configparser
import os
from datetime import datetime
import redis


class Task(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.readfp(open(os.path.join(os.path.dirname(__file__), "config.ini")))
        self.host = config.get("LOCAL_REDIS", "Host")
        self.port = config.get("LOCAL_REDIS", "Port")
        self.redis = redis.Redis(self.host, self.port)

    def main(self):
        global audio_url
        f_list = os.listdir(path)
        for audio_url in f_list:
            if os.path.splitext(audio_url)[1] == '.mp3' and not self.redis.sismember("audio_local_url", audio_url):
                break
        if audio_url:
            time_now = '您好，现在时间：%s，即将播放 一零二四好项目：' % datetime.now().strftime("%H:%M")
            url = 'http://tts.baidu.com/text2audio?idx=1&cuid=baidu_speech_' \
                  'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=10&pit=6&tex={0}'.format(time_now)
            print(url)
            os.system('mplayer "%s"' % url)
            os.system('mplayer  -af volume=+15  "%s/%s"' % (path, audio_url))
            self.redis.sadd("audio_local_url", audio_url)

if __name__ == '__main__':
    path = '~/Downloads/1024好项目'
    Task().main()
