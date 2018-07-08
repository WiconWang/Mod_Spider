# coding=utf-8
import time

import os

import cv2
import random


def division(path, path2):
    file_list = os.listdir(path)
    for file in file_list:
        if os.path.splitext(file)[1] != '.mp4':
            continue

        # 定义此文件号
        file_temp = "temp" + time.strftime('_%Y%m%d_%H%M%S_', time.localtime())
        file_capture = cv2.VideoCapture(path + file)

        # 判断视频是否打开
        if not file_capture.isOpened():
            return False

        # 获取原视频的帧率
        fps = file_capture.get(cv2.CAP_PROP_FPS)
        # 获取原视频帧的大小
        size = (int(file_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(file_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        # 获取原视频的总帧数
        frame_count = file_capture.get(cv2.CAP_PROP_FRAME_COUNT)
        # 定义帧计数
        i = 1
        # 定义文件序号
        j = 1

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video_writer = cv2.VideoWriter(path2 + file_temp + str(j) + '.mp4', fourcc, random.randint(-4, 4) + fps, size)

        # 读第一帧
        success, frame = file_capture.read()

        print("正在启动文件分割" + file)
        while success:
            # 写此文件
            video_writer.write(frame)
            i = i + 1
            # 每900帧截成一个新文件
            if i % 900 == 0:
                print("已完成：" + str(int(i / frame_count * 100)) + "%")
                j = j + 1
                # 声明新文件，且对fps进行变速
                video_writer = cv2.VideoWriter(path2 + file_temp + str(j) + '.mp4', fourcc,
                                               random.randint(-20, 20) + fps, size)
            # 加载 下一个文件
            success, frame = file_capture.read()
        print("分割完成" + file)

        merge(path2, file, file_temp, j, fps, size)
        # return j


# 传入 生成目标位置，文件名， 临时文件名，临时文件最大号，原文件fps，原文件size
def merge(path, file, file_temp, j, fps, size):
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    file_capture = cv2.VideoCapture(path + file_temp + str(1) + '.mp4')
    # 判断视频是否打开
    if not file_capture.isOpened():
        return False

    # 定义最终文件
    video_writer = cv2.VideoWriter(path + file, fourcc, fps, size)
    for i in range(1, j):
        file_capture = cv2.VideoCapture(path + file_temp + str(i) + '.mp4')
        # 判断视频是否打开
        if not file_capture.isOpened():
            return False

        # 读第一帧
        success, frame = file_capture.read()

        print("正在合并文件" + file + "(" + str(i) + "/" + str(j) + ")")
        while success:
            video_writer.write(frame)
            success, frame = file_capture.read()
        os.remove(path + file_temp + str(i) + '.mp4')
    print("合并文件" + file + "(完成)")
    try:
        os.remove(path + file_temp + str(j) + '.mp4')
    except Exception as e:
        pass


if __name__ == '__main__':
    try:
        # 硬盘路径(原视频存放路径)
        path = os.path.dirname(os.path.realpath(__file__)) + "/"
        # 切割后的视频存放路径
        path2 = path + "process"
        if not os.path.exists(path2):
            os.mkdir(path2, 0o777)
        if not os.path.exists(path2):
            print("警告，程序出错。无法新建process文件夹，请手动建立")
        else:
            path2 = path2 + "/"
            division(path, path2)
    except Exception as e:
        print("警告，程序出错:")
        print(e)
