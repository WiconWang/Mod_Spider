# coding:utf8

import os
import sys
import time
import subprocess
# import self
from PIL import Image
# 使用第三方库：Pillow
import math
import operator
import sys
from functools import reduce
from qiniu import Auth, put_file

from config import (
    URI_PREFIX, ACCESS_KEY, SECRET_KEY, BUCKET_NAME
)


class Diff:
    def pics(self, file1, file2):
        # 把图像对象转换为直方图数据，存在list h1、h2 中
        h1 = Image.open(file1).histogram()
        h2 = Image.open(file2).histogram()
        return math.sqrt(reduce(operator.add, list(
            map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
        # sqrt:计算平方根，reduce函数：前一次调用的结果和sequence的下一个元素传递给operator.add
        # operator.add(x,y)对应表达式：x+y
        # 这个函数是方差的数学公式：S^2= ∑(X-Y) ^2 / (n-1)


class UploadMain:
    global temp

    def __init__(self, *args, **kwargs):
        pass

    def upload(self, path, access_key, secret_key, bucket_name):
        """上传文件到七牛云空间    :param path: 文件路径     """
        # 构建鉴权对象
        auth = Auth(access_key, secret_key)
        key = os.path.split(path)[-1]
        # 生成上传 Token，可以指定过期时间等
        token = auth.upload_token(bucket_name, key, 3600)
        ret, _ = put_file(token, key, path)
        return ret and ret['key'] == key

    def process(self, img_path):
        """主流程"""

        # 检查七牛相关配置是否已配置
        if not all((URI_PREFIX, ACCESS_KEY, SECRET_KEY, BUCKET_NAME)):
            return [1, '请先设置七牛相关配置!']

        file_name = os.path.split(img_path)[-1]
        file_type = file_name.split('.')[-1]
        if file_type == 'tiff':
            new_img_path = '/tmp/{}.png'.format(int(time.time()))
            # tiff --> png
            self._convert_to_png(img_path, new_img_path)
            img_path = new_img_path

        try:
            # 上传到七牛
            upload_result = self.upload(
                img_path, ACCESS_KEY, SECRET_KEY, BUCKET_NAME)
            if not upload_result:
                return [1, '上传图片到七牛失败,请检查七牛相关配置是否正确!!']

            # 完整的七牛图片URI
            img_file_name = os.path.split(img_path)[-1]
            img_uri = '{}/{}'.format(URI_PREFIX, img_file_name)

        except Exception as error:
            return [1, '上传图片到七牛异常!{}'.format(str(error))]

        return [0, img_uri]

    def _convert_to_png(self, src_path, dest_path):
        """转换图片格式为png

        :param src_path: 源文件
        :param dest_path: 目标文件
        """
        os.system('sips -s format png {} --out {}'.format(src_path, dest_path))


class SendMessage:
    def __init__(self):
        pass

    def weixin(self, url):
        return [0, 'WXerror'+ url]


if __name__ == '__main__':
    # 初始页面并启动流程
    # if sys.argv[1]:
    #     process(sys.argv[1])
    # pass
    res = 0
    # 鉴定两个图差别
    if sys.argv[1] and sys.argv[2]:
        diffClass = Diff()
        res = diffClass.pics(sys.argv[1], sys.argv[2])

    if res > 3000:
        # 如果差别过大，则上传1号图片图片
        uploadClass = UploadMain()
        urls = uploadClass.process(sys.argv[1])
        # 上传步骤无错误时，进行去发送微信通知
        if urls[0] == 0:
            messageClass = SendMessage()
            msg = messageClass.weixin('http://'+urls[1])
            print('成功')
            print(msg)
        else:
            print(urls[1])