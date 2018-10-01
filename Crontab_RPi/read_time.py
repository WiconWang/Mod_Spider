# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import time


def main():
    text = '现在时间：' + time.strftime('%H:%M', time.localtime(time.time()))
    print(text)
    url = 'http://tts.baidu.com/text2audio?idx=1&tex={0}&cuid=baidu_speech_' \
          'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=10&pit=8'.format(text)
    # 直接播放语音
    os.system('mplayer "%s"' % url)


if __name__ == '__main__':
    main()
