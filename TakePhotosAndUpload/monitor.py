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

    def calculate(self, image1, image2):
        g = image1.histogram()
        s = image2.histogram()
        assert len(g) == len(s), "error"

        data = []

        for index in range(0, len(g)):
            if g[index] != s[index]:
                data.append(1 - abs(g[index] - s[index]) / max(g[index], s[index]))
            else:
                data.append(1)

        return sum(data) / len(g)

    def split_image(self, image, part_size):
        pw, ph = part_size
        w, h = image.size

        sub_image_list = []

        assert w % pw == h % ph == 0, "error"

        for i in range(0, w, pw):
            for j in range(0, h, ph):
                sub_image = image.crop((i, j, i + pw, j + ph)).copy()
                sub_image_list.append(sub_image)

        return sub_image_list

    def classfiy_histogram_with_split(self, image1, image2, size=(640, 480), part_size=(32, 24)):
        '''
         'image1' 和 'image2' 都是Image 对象.
         可以通过'Image.open(path)'进行创建。
         'size' 重新将 image 对象的尺寸进行重置，默认大小为256 * 256 .
         'part_size' 定义了分割图片的大小.默认大小为64*64 .
         返回值是 'image1' 和 'image2'对比后的相似度，相似度越高，图片越接近，达到100.0说明图片完全相同。
        '''
        img1 = image1.resize(size).convert("L")
        sub_image1 = self.split_image(img1, part_size)

        img2 = image2.resize(size).convert("L")
        sub_image2 = self.split_image(img2, part_size)

        sub_data = 0
        for im1, im2 in zip(sub_image1, sub_image2):
            sub_data += self.calculate(im1, im2)

        x = size[0] / part_size[0]
        y = size[1] / part_size[1]

        pre = round((sub_data / (x * y)), 6)
        return pre * 100

    # def getImgHash(self, fne):
    #     image_file = Image.open(fne)  # 打开
    #     image_file = image_file.resize((12, 12))  # 重置图片大小我12px X 12px
    #     image_file = image_file.convert("L")  # 转256灰度图
    #     Grayls = getGray(image_file)  # 灰度集合
    #     avg = getAvg(Grayls)  # 灰度平均值
    #     bitls = ''  # 接收获取0或1
    #     # 除去变宽1px遍历像素
    #     for h in range(1, image_file.size[1] - 1):  # h
    #         for w in range(1, image_file.size[0] - 1):  # w
    #             if image_file.getpixel((w, h)) >= avg:  # 像素的值比较平均值 大于记为1 小于记为0
    #                 bitls = bitls + '1'
    #             else:
    #                 bitls = bitls + '0'
    #     return bitls
    #
    # def pics(self, file1, file2):
    #     # 把图像对象转换为直方图数据，存在list h1、h2 中
    #     h1 = Image.open(file1).histogram()
    #     h2 = Image.open(file2).histogram()
    #     return math.sqrt(reduce(operator.add, list(
    #         map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
    #     # sqrt:计算平方根，reduce函数：前一次调用的结果和sequence的下一个元素传递给operator.add
    #     # operator.add(x,y)对应表达式：x+y
    #     # 这个函数是方差的数学公式：S^2= ∑(X-Y) ^2 / (n-1)


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
        return [0, 'WXerror' + url]


if __name__ == '__main__':
    # 初始页面并启动流程
    # if sys.argv[1]:
    #     process(sys.argv[1])
    # pass
    res = 100
    # 鉴定两个图差别
    if sys.argv[1] and sys.argv[2]:
        diffClass = Diff()
        res = diffClass.classfiy_histogram_with_split(Image.open(sys.argv[1]), Image.open(sys.argv[2]))

    # 相似度低于75时，上传图片
    # print(sys.argv[1] + " + " + sys.argv[2] + "  : " + str(res))
    if res < 75:
        # 如果差别过大，则上传1号图片图片
        uploadClass = UploadMain()
        urls = uploadClass.process(sys.argv[1])
        # 上传步骤无错误时，进行去发送微信通知
        if urls[0] == 0:
            # messageClass = SendMessage()
            # msg = messageClass.weixin('http://' + urls[1])
            print("WARING" + sys.argv[1] + " + " + sys.argv[2] + "  : " + str(res))
        else:
            print(sys.argv[1] + " + " + sys.argv[2] + "  : " + str(res))

