# -*- coding: utf-8 -*-
import configparser
import os
import random


def main(mp3path):
    print(mp3path)
    # 先播放一首音乐做闹钟
    os.system('mplayer  -af volume=+0 %s' % mp3path)


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
    music_path = config.get("RAND_MUSIC", "path")
    main(rand(music_path))
