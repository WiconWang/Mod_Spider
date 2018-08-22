# -*- coding: utf-8 -*-
# 读取指定目录文件名，并播放
import os
# from datetime import datetime
# import redis
import requests
import time
import hashlib
import base64


class Task(object):
    def __init__(self):
        self.URL = "http://api.xfyun.cn/v1/service/v1/tts"
        self.AUE = "lame"
        self.APP_ID = "2"
        self.API_KEY = "1"
        # 硬盘路径(原视频存放路径)
        self.SOURCE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/txt/"
        # 切割后的视频存放路径
        self.RESOURCE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/audio/"

    def getHeader(self):
        curTime = str(int(time.time()))
        param = "{\"aue\":\"" + self.AUE + "\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"xiaoyan\",\"engine_type\":\"intp65\"}"
        paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
        m2 = hashlib.md5()
        m2.update((self.API_KEY + curTime + paramBase64).encode("utf8"))
        checkSum = m2.hexdigest()
        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': self.APP_ID,
            'X-CheckSum': checkSum,
            'X-Real-Ip': '127.0.0.1',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

    def getBody(self, text):
        data = {'text': text}
        return data

    def writeFile(self, file, content):
        with open(file, 'wb') as f:
            f.write(content)
        f.close()

    def convert(self, txt):
        try:
            r = requests.post(self.URL, headers=self.getHeader(), data=self.getBody(txt))
            contentType = r.headers['Content-Type']
            if contentType == "audio/mpeg":
                sid = r.headers['sid']
                if self.AUE == "raw":
                    self.writeFile(self.RESOURCE_PATH + sid + ".wav", r.content)
                else:
                    self.writeFile(self.RESOURCE_PATH + sid + ".mp3", r.content)
                print("success, sid = " + sid)
            else:
                print(r.text)
        except Exception as e:
            print('警告，出现错误:')
            print('行号：', e.__traceback__.tb_lineno)
            print('错误：', e)

    def validTime(self):
        return int(time.time()) < 1534584028 + 30 * 24 * 60 * 60

    def validFolder(self):
        if not os.path.exists(self.SOURCE_PATH):
            os.mkdir(self.SOURCE_PATH, 0o777)
        if not os.path.exists(self.SOURCE_PATH):
            print("警告，程序出错。无法新建 TXT 文件夹，请手动建立")
            return False

        if not os.path.exists(self.RESOURCE_PATH):
            os.mkdir(self.RESOURCE_PATH, 0o777)
        if not os.path.exists(self.RESOURCE_PATH):
            print("警告，程序出错。无法新建 音频 文件夹，请手动建立")
            return False
        return True

    def main(self):
        if not Task().validTime():
            print("过期了，找隔壁的老王再要一份吧。。")
            return False

        if not Task().validFolder():
            print("请手动创建 txt 文件夹和 audio 文件夹。。")
            return False
        content = "科大讯飞是中国最大的智能语音技术提供商"
        Task().convert(content)
        return True


if __name__ == '__main__':
    Task().main()

    name = input("程序结束!")
    print(name)
