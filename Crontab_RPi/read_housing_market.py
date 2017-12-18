# -*- coding: utf-8 -*-
# 取线上采集的三十天的楼市数据
import os
import requests
import json
from datetime import *


class Task(object):
    def __init__(self):
        self.city = ["bj", "qd", "jn"]
        self.city_name = ["北京", "青岛", "济南"]

    def main(self):
        thisweek = datetime.now().weekday()
        city = ''
        if thisweek == 5:
            city = self.city[2]
            city_name = self.city_name[2]
        if thisweek == 0:
            city = self.city[0]
            city_name = self.city_name[0]
        if thisweek == 2:
            city = self.city[1]
            city_name = self.city_name[1]

        if city == '':
            return False

        month = date.today().strftime("%Y%m")
        json = self.getjson('http://data.huiye360.com/Mod_Scrapy/public/last_%s_%s.json' % (city, month))

        if json:
            start_date = json['start_date']
            end_date = json['end_date']
            days = (datetime.strptime(start_date, "%Y-%m-%d") - datetime.strptime(end_date, "%Y-%m-%d")).days

            str = "您好，现在时间：%s，今天播报 %s市 最近%s天房价走势：" % (datetime.now().strftime("%H:%M"), city_name, days)
            for val in json['counts']:
                if json['counts'][val]['_id'] != '':
                    str += " %s区：%s个样本，平均房价为%s元。" %(json['counts'][val]['_id'], json['counts'][val]['count'], int(json['counts'][val]['preprice']))


            url = 'http://tts.baidu.com/text2audio?idx=1&cuid=baidu_speech_' \
                  'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=5&vol=10&pit=6&tex={0}'.format(str)
            # 直接播放语音
            os.system('mplayer "%s"' % url)

    def getjson(self, url):

        # 请求远端服务器并选取JSON
        r = requests.get(url=url)
        if r.status_code != 200:
            print('404 Error')
            return False
        return r.json()


if __name__ == '__main__':
    Task().main()
