# coding=utf-8
import time
import os
import subprocess
import random


def substring(date):
    r = date.decode()
    r = r.strip()
    rlist = r.split(":")
    result = (int(rlist[0]) * 60 * 60) + (int(rlist[1]) * 60) + (float(rlist[2]))
    return result


def division(path, path2):
    file_list = os.listdir(path)
    for file in file_list:
        if os.path.splitext(file)[1] != '.mp4':
            continue

        # 定义此文件号
        file_temp = time.strftime('_%Y%m%d_%H%M%S_', time.localtime())
        file_temp_step1 = file_temp + "step1_"

        # 获取当前文件的视频长度
        strcmd = ["ffmpeg -y -i " + path + file + " 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//"]
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        date = result.stdout
        video_time = substring(date)

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
        step_time = 60
        print("* 对文件:" + str(file) + " 的切片调速合并工作已开启！")
        print("* 预计会有 " + str(int(video_time / step_time)+1) + " 个文件碎片产生")
        while start < video_time * 100:
            end = start + step_time * 100

            if end > video_time * 100:
                end = video_time * 100
                step_time = (end - start) / 100
            sub = "ffmpeg -y -accurate_seek -i " + path + file + " -ss " + str(
                start / 100) + "  -r 30   -t " + str(step_time) + " " + path2 + file_temp_step1 + str(
                count) + '.mp4 -loglevel quiet'
            video_result = subprocess.run(args=sub, shell=True)
            # print(video_result)
            print("- 文件第" + str(count) + "片，已成功分离")
            adjust(path2, count, file_temp)
            start = end
            count = count + 1

        merge(path2, file, file_temp, count - 1)


def adjust(path, count, file_temp):
    file_step1 = path + file_temp + "step1_" + str(count) + '.mp4'
    file_step2 = path + file_temp + "step2_" + str(count) + '.mp4'
    # 本碎片的速度
    pts = random.randint(5, 20) / 10
    if pts == 1:
        pts = 1.1
    sub = 'ffmpeg -y -i ' + file_step1 + ' -r 30 -filter_complex "[0:v]setpts=' \
          + str(pts) + '*PTS[v];[0:a]atempo=' + str(
        pts) + '[a]" -map "[v]" -map "[a]" ' + file_step2 + '  -loglevel quiet'
    video_result = subprocess.run(args=sub, shell=True)
    # print(video_result)
    print("- 文件碎片" + str(count) + "号的速度，已调整为" + str(pts) + "倍")
    return True


# 传入 生成目标位置，文件名， 临时文件名，临时文件最大号，原文件fps，原文件size
def merge(path, file, file_temp, count):
    print(count)
    all_file = ''
    for i in range(1, count + 1):
        sub_part = 'ffmpeg –i  process/' + file_temp + "step2_" + str(i)\
                   + '.mp4 –vcodec copy –acodec copy –vbsf part_' + str(i) + '.ts'
        print(sub_part)
        video_result = subprocess.run(args=sub_part, shell=True)
        all_file = all_file + 'part_' + str(i) + '.ts|'
    all_file = all_file[0:len(all_file) - 1]
    print("+ 正在合并文件碎片" + file + " ")
    sub = 'ffmpeg -i "concat:'+all_file+'" -acodec copy -vcodec copy -absf aac_adtstoasc ' + path + file + ' -loglevel quiet'
    # sub = 'ffmpeg -y -i "concat:' + all_file + '" -c copy ' + path + file + ' -loglevel quiet'
    print(sub)
    video_result = subprocess.run(args=sub, shell=True)

    # for i in range(1, count + 1):
    #     os.remove(path + file_temp + "step1_" + str(i) + '.mp4')
    #     os.remove(path + file_temp + "step2_" + str(i) + '.mp4')
    print("* 工作完成：" + file + "，请到 process 文件夹下 拷走 此文件！")


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
