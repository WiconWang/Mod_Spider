# -*- coding: utf-8 -*-
import configparser
import os
import random
import time


def main(mp3path, readText):
    text = "现在 " + time.strftime('%H:%M', time.localtime(time.time())) + " " + readText
    print(text)
    url = 'http://tts.baidu.com/text2audio?idx=1&tex={0}&cuid=baidu_speech_' \
          'demo&cod=2&lan=zh&ctp=1&pdt=1&spd=4&per=4&vol=10&pit=8'.format(text)
    # 直接播放语音
    os.system('mplayer "%s"' % url)
    time.sleep(1)
    # 先播放一首音乐做闹钟
    os.system('mplayer  -af volume=+5 %s' % mp3path)


def rand(music_path):
    global parent
    file_names = []
    for parent, folder, files in os.walk(music_path):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for single_file in files:
            if str(single_file).startswith('._') or not str(single_file).endswith('mp3'):
                pass
            else:
                file_names.append(os.path.join(parent, single_file))
    x = random.randint(0, len(file_names) - 1)
    return file_names[x]


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.readfp(open(os.path.join(os.path.dirname(__file__), "config.ini")))
    # 早晨和晚上分别放不同的文件夹内容
    if int(time.strftime('%H', time.localtime(time.time()))) < 12:
        main(rand(config.get("RAND_MUSIC", "path")), "快点起床了！")
    else:
        main(rand(config.get("RAND_MUSIC", "path_night")), "准备睡觉了！")
