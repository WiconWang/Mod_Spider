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
        source_json = self.getjson('http://www.weather.com.cn/data/sk/101120201.html')
        if not source_json:
            return False
        city =source_json['weatherinfo']['city']
        print(source_json)
        print(city.decode('utf-8') )
        print(source_json['weatherinfo']['WD'])
        # today_suggest = '天气%s, %s' %(jn_json['weather'][0]['today']['suggestion']['dressing']['brief'], jn_json['weather'][0]['today']['suggestion']['dressing']['details'])
        # today_suggest = '天气%s' %(jn_json['weather'][0]['today']['suggestion']['dressing']['brief'])
        # now_aqi = '污染指数：%s，空气质量：%s' % (jn_json['weather'][0]['now']['air_quality']['city']['aqi'], jn_json['weather'][0]['now']['air_quality']['city']['quality'])
        # today_weather = self.formatWeather(today_dict['text'])
        #
        # # 指定第二地点天气
        # fx_str = ''
        # fx_json = self.getjson('http://tj.nineton.cn/Heart/index/all?city=CHSD080800')
        # if fx_json:
        #     fx_dict = fx_json['weather'][0]['future'][0]
        #     fx_weather = self.formatWeather(fx_dict['text'])
        #     fx_str = '临沂市费县，今天%s,最高%s度, 最低%s度, %s' % (fx_weather, fx_dict['high'],fx_dict['low'],fx_dict['wind'])
        #
        # str = '现在%s，今天是%s, 济南今天 %s,最高%s度, 最低%s度, %s ,%s, %s 。 %s' % (datetime.now().strftime("%H:%M"), today_dict['day'],today_weather,today_dict['high'],today_dict['low'],today_dict['wind'], today_suggest, now_aqi, fx_str)
        #
        # url = 'http://tts.baidu.com/text2audio?idx=1&cuid=baidu_speech_' \
        #       'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=10&pit=6&tex={0}'.format(str)
        # print(str)
        # # 直接播放语音
        # os.system('mplayer "%s"' % url)
        pass

    def formatWeather(self,weather):
        today_weather = weather
        if "/" in weather:
            t1 = weather.split('/')
            if t1[0] == t1[1]:
                today_weather = t1[0]
            else:
                today_weather = '%s转%s' % (t1[0], t1[1])
        return today_weather

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
