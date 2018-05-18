# coding:utf8
from PIL import Image
# 使用第三方库：Pillow
import math
import operator
import sys
from functools import reduce


def diff_pics(file1, file2):
    # 把图像对象转换为直方图数据，存在list h1、h2 中
    h1 = Image.open(file1).histogram()
    h2 = Image.open(file2).histogram()
    return math.sqrt(reduce(operator.add, list(
        map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
    # sqrt:计算平方根，reduce函数：前一次调用的结果和sequence的下一个元素传递给operator.add
    # operator.add(x,y)对应表达式：x+y
    # 这个函数是方差的数学公式：S^2= ∑(X-Y) ^2 / (n-1)


def send_message():
    pass


def main():
    res = 0
    if sys.argv[1] and sys.argv[2]:
        res = diff_pics(sys.argv[1], sys.argv[2])
    print(res)


if __name__ == '__main__':
    main()
