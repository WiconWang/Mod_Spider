# -*- coding:utf-8 -*-
import datetime
import itertools
import time
import os
import subprocess
import random


def validateTitle(title):
    try:
        # print(''.join(title))
        title = title.strip()
        title = title.replace(' ', str(random.randint(0, 9)))
        title = title.replace('　', str(random.randint(0, 9)))
        title = title.replace('&', str(random.randint(0, 9)))
        title = title.replace('#', str(random.randint(0, 9)))
        title = title.replace('`', str(random.randint(0, 9)))
        title = title.replace('%', str(random.randint(0, 9)))
        title = title.replace('\'', str(random.randint(0, 9)))
        title = title.replace('"', str(random.randint(0, 9)))
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



def getValid():
    return int(time.time()) < 1535698955 + 30 * 24 * 60 * 60


def getFullList(path):
    try:
        fullList = []
        for file in os.listdir(path):
            if os.path.splitext(file)[1] != '.mp4':
                continue
            fullList.append(file)

        if len(fullList) > 10:
            return fullList
        else:
            print('警告，产生不连续的5段拼合，最少需要10个视频:')
            name = input("程序已退出，请注意!")
            print(name)

    except Exception as e:
        print('警告，检索文件列表出错:')
        print('行号：', e.__traceback__.tb_lineno)
        print('错误：', e)
        name = input("程序已退出，请注意!")
        print(name)


# 取得所有文件数，非连续的组合方案
def getLastList(counts, num):
    lastList = []
    # 生成所有的排序方案
    for scheme in itertools.combinations(range(1, counts), num):
        listI = list(scheme)
        check = 1
        for j in range(len(listI) - 1):
            if listI[j] + 1 == listI[j + 1]:
                check = 0
                break
        if check == 1:
            lastList.append(scheme)
    return lastList


# 在所有方案中，取出x个方案
def getRandList(fullList, outNum):
    if len(fullList) > outNum:
        return random.sample(fullList, outNum)
    else:
        return fullList


def randMerge(fileList, scheme, inPath, outPath):
    listScheme = list(scheme)
    resFiles = ''
    try:
        # all_file = ''
        sub = 'ffmpeg  -y'
        filter_complex = ' -filter_complex "'
        for i in range(len(listScheme)):
            sub += ' -i ' + os.path.dirname(os.path.realpath(__file__)) + '/' + inPath + '/' + fileList[listScheme[i]]
            filter_complex += ' [' + str(i) + ':0] [' + str(i) + ':1] '
            resFiles += fileList[listScheme[i]] + " -> "
        sub += ' -r 25 ' + filter_complex + 'concat=n=' + str(
            len(listScheme)) + ':v=1:a=1 [v] [a]" -map "[v]" -map "[a]" ' + os.path.dirname(
            os.path.realpath(__file__)) + '/' + outPath + '/' + \
               datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.mp4  -loglevel quiet'

        print("+ 合并方案启动：" + str(resFiles) + "尾标 ")
        video_result = subprocess.run(args=sub, shell=True)
        time.sleep(2)
        print("* 工作完成：" + outPath + "，请到 process 文件夹下 拷走 此文件！")
        print("---")
    except Exception as e:
        print('警告，融合视频出现错误:')
        print('行号：', e.__traceback__.tb_lineno)
        print('错误：', e)
        name = input("程序已退出，请注意!")
        print(name)


if __name__ == '__main__':
    perFrag = 5  # 每个视频用几个小视频拼出
    outNum = 10  # 最终输出6个视频
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
                # # print('---')
                # 全部改名
                renameFile(path + "/", path2 + "/")
                # 取得所有文件清单
                fileList = getFullList("source")
                print("* 检测到" + str(len(fileList)) + "个文件")
                # 取得所有方案
                scheme = getLastList(len(fileList), perFrag)
                print("* 从组合结果中筛选出 " + str(len(scheme)) + " 个方案")
                # 从所有方案中随机选出几条方案
                randScheme = getRandList(scheme, outNum)
                print("* 最终确定 " + str(outNum) + " 个方案")
                # 对每个方案进行逐个实现
                count = 0
                for i in range(len(randScheme)):
                    print("* 开始生成第" + str(i + 1) + "个视频")
                    randMerge(fileList, randScheme[i], 'source', 'process')
                    count = count + 1
                name = input("END: 工作完成，产生!" + str(count) + "个视频")
                print(name)
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
