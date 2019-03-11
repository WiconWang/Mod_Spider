# -*- coding:utf-8 -*-

import time
import os
import subprocess
import random
import platform
import re

def validateTitle(title):
    try:
        # print(''.join(title))
        title = title.strip()
        title = title.replace(' ',str(random.randint(0,9)))
        title = title.replace('　',str(random.randint(0,9)))
        title = title.replace('&',str(random.randint(0,9)))
        title = title.replace('#',str(random.randint(0,9)))
        title = title.replace('`',str(random.randint(0,9)))
        title = title.replace('%',str(random.randint(0,9)))
        title = title.replace('\'',str(random.randint(0,9)))
        title = title.replace('"',str(random.randint(0,9)))
        # rstr = r'[\\/:*?"<>|\r\n]+'
        # rstr = r'[-?{[|#$%@^&*() -`%,/\';:~!\ $]'
        # new_title = re.sub(rstr, "_", title)  # 替换为下划线
        # new_title = re.sub(rstr, , title)  # 替换为下划线
        return title

    except Exception as e:
        print('警告，文件名替换出现错误:')
        print('行号：', e.__traceback__.tb_lineno)
        print('错误：', e)
        name = input("程序已退出，请注意!")
        print(name)

def substring(date):
    try:
        r = date.decode()
        r = r.replace('Duration:', '').strip()
        r1 = r.split(",")
        rlist = r1[0].split(":")
        result = (int(rlist[0]) * 60 * 60) + (int(rlist[1]) * 60) + (float(rlist[2]))
        return result

    except Exception as e:
        print('警告，视频时间检测出现错误:')
        print('行号：', e.__traceback__.tb_lineno)
        print('错误：', e)
        name = input("程序已退出，请注意!")
        print(name)

def renameFile(path, path2):
    try:
        file_list = os.listdir(path)
        for file in file_list:
            newfile = validateTitle(file)
            if newfile != file:
                 os.rename(path + file, path + newfile)

    except Exception as e:
        print('警告，更新视频文件名出现错误:')
        print('行号：', e.__traceback__.tb_lineno)
        print('错误：', e)
        name = input("程序已退出，请注意!")
        print(name)

def division(path, path2):
    try:
        file_list = os.listdir(path)
        for file in file_list:
            if os.path.splitext(file)[1] != '.mp4':
                continue

            print("* 对文件:" + str(file) + " 的切片调速合并工作已开启！")
            # 定义此文件号
            file_temp = time.strftime('_%Y%m%d_%H%M%S_', time.localtime())
            file_temp_step1 = file_temp + "step1_"

            # print('----')
            # print(file)
            # 检测是否有srt的汉字字幕，如果有，先合并
            file_srt = os.path.splitext(file)[0] + '.zh-CN.srt'
            if os.path.exists(file_srt):
                print("* 检测到字幕:" + str(file_srt) + " 正在合并！")
                subsrt = 'ffmpeg -y -i ' + path + file + ' -i ' + path + file_srt + ' -vf  subtitles=' + path + file_srt + ' ' + file_temp + 'srt.mp4 -loglevel quiet'
                video_result = subprocess.run(args=subsrt, shell=True)
                file = file_temp + 'srt.mp4'

            # 检测终端类型并选择不同命令
            cmd_grep = ("find" if ('Windows' in platform.system()) else "grep")
            strcmd = 'ffmpeg -y -i ' + path + file + ' 2>&1 | ' + cmd_grep + ' "Duration"'
            # print(strcmd)

            result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
            date = result.stdout
            # print(date)
            # 解析出具体的时间
            video_time = substring(date)

            if not video_time or video_time == 0:
                print("无法解析此文件时间")
                break
            # print(type(date))
            # print(date)
            # print(file_temp_step1)
            # print(video_time)  # 162.32
            #

            # 把数值升到整数，1秒为100
            start = 0
            end = 1
            count = 1
            # 每小节时间，单位秒
            # step_time = 60

            # 目前要求固定四小段
            # print(video_time)
            # 计算基础时间
            step_time = int(video_time / 4) + 1
            step_time_rand_start = step_time - int(step_time / 2)
            step_time_rand_end = step_time + int(step_time / 2)

            step_time_list = []
            # 对前三段时间进行随机
            step_time_list.append(round(random.randint(step_time_rand_start, step_time_rand_end), 2))
            step_time_list.append(round(random.randint(step_time_rand_start, step_time_rand_end), 2))
            step_time_list.append(round(random.randint(step_time_rand_start, step_time_rand_end), 2))

            # 第四段时间进行处理
            step_time_list.append(round((video_time - step_time_list[0] - step_time_list[1] - step_time_list[2]), 2))
            # print(step_time_list)

            # print("* 预计会有 " + str(int(video_time / step_time) + 1) + " 个文件碎片产生")
            print("* 已固定产出 4 个文件碎片")
            while start < video_time * 100:
                # 查一下界标，如果超过了则跳出此步骤，解决小数精度问题
                if count > len(step_time_list):
                    break
                step_time = step_time_list[count - 1]
                end = start + step_time_list[count - 1] * 100

                if end > video_time * 100:
                    end = video_time * 100
                    step_time = (end - start) / 100
                sub = "ffmpeg -y -accurate_seek -i " + path + file + " -ss " + str(
                    start / 100) + "  -r 30   -t " + str(step_time) + " " + path2 + file_temp_step1 + str(
                    count) + '.mp4 -loglevel quiet'
                video_result = subprocess.run(args=sub, shell=True)
                # print(video_result)
                print("- 文件第" + str(count) + "片，已成功分离，" + str(start / 100) + "至" + str(end / 100) + "秒")

                file_step1 = path2 + file_temp + "step1_" + str(count) + '.mp4'
                file_step2 = path2 + file_temp + "step2_" + str(count) + '.mp4'
                # 本碎片的速度
                pts = random.randint(95, 105) / 100
                if pts == 1:
                    pts = 1.1
                # 声音和视频正好相反，因此取反
                pts_audio = int((1 / pts) * 100) / 100
                sub = 'ffmpeg -y -i ' + file_step1 + ' -r 25 -filter_complex "[0:v]setpts=' \
                      + str(pts) + '*PTS[v];[0:a]atempo=' + str(
                    pts_audio) + '[a]" -map "[v]" -map "[a]" ' + file_step2 + '  -loglevel quiet'
                video_result = subprocess.run(args=sub, shell=True)
                # print(video_result)
                print("- 文件碎片 " + str(count) + "号的速度，已调整为" + str(pts) + "倍")

                start = end
                count = count + 1

            time.sleep(2)
            merge(path2, file, file_temp, count - 1)
        print("---")
        input("任务已完成，请关闭窗口")
    except Exception as e:
        print('警告，修整视频出现错误:')
        print('行号：', e.__traceback__.tb_lineno)
        print('错误：', e)
        name = input("程序已退出，请注意!")
        print(name)


# 传入 生成目标位置，文件名， 临时文件名，临时文件最大号，原文件fps，原文件size
def merge(path, file, file_temp, count):
    try:
        # all_file = ''
        sub = 'ffmpeg  -y'
        filter_complex = ' -filter_complex "'
        for i in range(1, count + 1):
            sub += ' -i  process/' + file_temp + "step2_" + str(i) + '.mp4 '
            filter_complex += ' [' + str(i - 1) + ':0] [' + str(i - 1) + ':1] '
        sub += ' -r 25 ' + filter_complex + 'concat=n=' + str(
            count) + ':v=1:a=1 [v] [a]" -map "[v]" -map "[a]" ' + path + file + '  -loglevel quiet'

        # ffmpeg -i process/_20180709_000404_step2_1.mp4
        # -i process/_20180709_000404_step2_2.mp4
        # -i process/_20180709_000404_step2_3.mp4
        # -i process/_20180709_000404_step1_1.mp4
        # -filter_complex '[0:0] [0:1] [1:0] [1:1] [2:0] [2:1] [3:0] [3:1] concat=n=4:v=1:a=1 [v] [a]' -map '[v]' -map '[a]' output.mp4
        # print(sub)
        print("+ 正在合并文件碎片 " + file + " 共" + str(count) + "块")
        video_result = subprocess.run(args=sub, shell=True)

        time.sleep(2)
        for i in range(1, count + 1):
            os.remove(path + file_temp + "step1_" + str(i) + '.mp4')
            os.remove(path + file_temp + "step2_" + str(i) + '.mp4')
        print("* 工作完成：" + file + "，请到 process 文件夹下 拷走 此文件！")
        print("---")
    except Exception as e:
        print('警告，融合视频出现错误:')
        print('行号：', e.__traceback__.tb_lineno)
        print('错误：', e)
        name = input("程序已退出，请注意!")
        print(name)


def getValid():
    return int(time.time()) < 1534584028 + 3000 * 24 * 60 * 60


if __name__ == '__main__':
    try:
        # 硬盘路径(原视频存放路径)
        path = os.path.dirname(os.path.realpath(__file__)) + "/source"
        # 切割后的视频存放路径
        path2 = os.path.dirname(os.path.realpath(__file__)) + "/process"
        if not os.path.exists(path2):
            os.mkdir(path2, 0o777)
        if not os.path.exists(path2):
            print("警告，程序出错。无法新建process文件夹，请手动建立")
        else:
            if getValid():
                # print('---')
                renameFile(path + "/", path2 + "/")
                division(path + "/", path2 + "/")
            else:
                print("过期了，找隔壁的老王再要一份吧。。")
        name = input("程序结束，请点击关闭")
        print(name)
    except Exception as e:
        print('警告，出现错误:')
        print('行号：', e.__traceback__.tb_lineno)
        print('错误：', e)
        name = input("程序已退出，请注意!")
        print(name)
