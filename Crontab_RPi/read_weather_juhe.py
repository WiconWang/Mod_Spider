# -*- coding: utf-8 -*-
# 取天气预报
import os
import requests
import json
from datetime import *



class ReadWeather(object):

    global temp

    def __init__(self):
        pass

    def main(self):
        jn_json = self.getjson('http://v.juhe.cn/weather/index?format=2&cityname=%E5%B4%82%E5%B1%B1&key=856677a58c47024c955dda9066c7bd11')
        if not jn_json:
            return False

        today_dict = jn_json['result']['today']
        # today_suggest = '天气%s, %s' %(jn_json['weather'][0]['today']['suggestion']['dressing']['brief'], jn_json['weather'][0]['today']['suggestion']['dressing']['details'])
        today_suggest = '天气%s' %(today_dict['dressing_index'])
        now_aqi = '污染指数：%s，空气质量：%s' % (1, 2)

        # 指定第二地点天气
        fx_str = ''
        fx_json = self.getjson('http://v.juhe.cn/weather/index?format=2&cityname=%E8%B4%B9%E5%8E%BF&key=856677a58c47024c955dda9066c7bd11')
        if fx_json:
            fx_dict = fx_json['result']['today']
            fx_str = '临沂今天%s,温度%s度, %s' % ( fx_dict['weather'], fx_dict['temperature'],fx_dict['wind'])

        str = '现在%s，今天是%s, 青岛今天 %s,温度%s, %s ,%s, %s 。 %s' % (datetime.now().strftime("%H:%M"), today_dict['week'],today_dict['weather'],today_dict['temperature'],today_dict['wind'], today_suggest, now_aqi, fx_str)

        url = 'http://tts.baidu.com/text2audio?idx=1&cuid=baidu_speech_' \
              'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=10&pit=6&tex={0}'.format(str)
        print(str)
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