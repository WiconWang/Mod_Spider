# -*- coding: utf-8 -*-
#  检测坐标1到坐标2的通勤情况，如果超过一小时,则发布播报。
import time
import os
import requests
import configparser



class Task(object):

    def __init__(self):
        config = configparser.ConfigParser()
        config.readfp(open('config.ini'))
        self.start = config.get("CHECK_BUS_TIME", "Start")
        self.end = config.get("CHECK_BUS_TIME", "End")
        self.ak = config.get("CHECK_BUS_TIME", "ak")

    def main(self):
        url = "http://api.map.baidu.com/direction/v2/transit"
        # 选择一系列地址，并查询最新一第是否已经在缓存 中有记录，如果有记录则找下一地址，直到找到一个最新的
        params = {'origin': self.start, 'destination': self.end,
                  'ak': self.ak, 'page_size': '3', 'tactics_incity': '3'}
        result = self.getjson(url, params)

        html = '注意：无法取得今日的路况和用时,请及时查询！注意，无法取得路况信息！'
        if result:
            if result['routes']:
                if result['routes'][0]['duration']:
                    secs = result['routes'][0]['duration']
                    minute = int(secs / 60)
                    # 出门的时间戳
                    time_stamp = time.mktime(time.strptime(time.strftime('%Y-%m-%d 09:00:00', time.localtime(time.time())),
                                                           '%Y-%m-%d %H:%M:%S')) - secs
                    # 转换成新的时间格式(2016-05-05 20:28:54)
                    lastTime = time.strftime("%H点%M分", time.localtime(time_stamp))

                    if minute > 60:
                        html = '警告： 今日路况耗时已超一小时，请注意提前出行，预计需要' + str(minute) + '分钟。'
                    else:
                        html = '路况播报： 今天预计需要' + str(minute) + '分钟。'
                    html += '您最晚应该在' + lastTime + '之前出门。距离' + lastTime + '，'

                    # 取 出门剩余时间
                    diff_minute = int((time_stamp - time.time()) / 60)
                    if diff_minute > 0:
                        html += '还有' + str(diff_minute) + '分钟准备'
                    else:
                        html += '已经超过了' + str(0 - diff_minute) + '分钟'

        # 语音合成

        url = 'http://tts.baidu.com/text2audio?idx=1&cuid=baidu_speech_' \
              'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=10&pit=6&tex={0}'.format(html)
        print(url)
        # 直接播放语音
        # os.system('mplayer "%s"' % url)

    def getjson(self, url, params):
        # 请求远端服务器并选取JSON
        r = requests.get(url=url, params=params)
        if r.status_code != 200:
            print('404 Error')
            return False
        if r.json()['status'] != 0:
            return False
        return r.json()['result']


if __name__ == '__main__':
    Task().main()
