# -*- coding: utf-8 -*-
# 取天气预报
import configparser
import os
import requests
import json
from datetime import *


class ReadWeather(object):
    global temp

    def __init__(self):
        config = configparser.ConfigParser()
        config.readfp(open('config.ini'))
        self.Area1_name = config.get("WEATHER", "Area1_name")
        self.Area2_name = config.get("WEATHER", "Area2_name")
        self.Key = config.get("WEATHER", "Juhe_Key")
        pass

    def main(self):
        jn_json = self.getjson(
            'http://v.juhe.cn/weather/index?format=2&cityname=%s&key=%s' % (self.Area1_name, self.Key))
        if not jn_json:
            return False

        today_dict = jn_json['result']['today']
        # today_suggest = '天气%s, %s' %(jn_json['weather'][0]['today']['suggestion']['dressing']['brief'],
        # jn_json['weather'][0]['today']['suggestion']['dressing']['details'])
        today_suggest = '天气%s' % (today_dict['dressing_index'])
        now_aqi = ''

        # 指定第二地点天气
        city2_str = ''
        city2_json = self.getjson(
            'http://v.juhe.cn/weather/index?format=2&cityname=%s&key=%s' % (self.Area2_name, self.Key))
        if city2_json:
            city2_dict = city2_json['result']['today']
            city2_str = '%s今天%s,温度%s度, %s' % (
                self.Area2_name, city2_dict['weather'], city2_dict['temperature'], city2_dict['wind'])

        weather = '现在%s，今天是%s, %s今天 %s,温度%s, %s ,%s, %s 。 %s' % (
            datetime.now().strftime("%H:%M"), today_dict['week'], self.Area1_name, today_dict['weather'],
            today_dict['temperature'], today_dict['wind'], today_suggest, now_aqi, city2_str)

        url = 'http://tts.baidu.com/text2audio?idx=1&cuid=baidu_speech_' \
              'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=10&pit=6&tex={0}'.format(weather)
        print(weather)
        # 直接播放语音
        os.system('mplayer "%s"' % url)
        pass

    def getjson(self, url):

        # 请求远端服务器并选取JSON
        r = requests.get(url=url)
        if r.status_code != 200:
            print('404 Error')
            return False
        return r.json()


if __name__ == '__main__':
    # 初始页面并启动流程
    ReadWeather().main()
    pass
