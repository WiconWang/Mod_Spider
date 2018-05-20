#!/bin/bash

# cd `dirname $0`
# nowtime=`date +%Y%m%d_%H%M%S`
# path="/home/pi/Monitor/Cam_$nowtime"
# fswebcam --no-banner -r 640x480 $path"1.jpg"
# #USB摄像头第一张一般都不清晰，所以一秒后再拍一张
# sleep 1
# fswebcam --no-banner -r 640x480 $path".jpg"
# python3 processer.py $path".jpg"
# rm -f $path"1.jpg"

cd `dirname $0`
folder="/home/pi/Monitor"
# 取上次的图片
last_file=`ls -t $folder/*.jpg | head -1`

# 开始拍图片
nowtime=`date +%Y%m%d_%H%M%S`
path=$folder"/Cam_$nowtime"

#USB摄像头第一张一般都不清晰，所以一秒后再拍一张
fswebcam --no-banner -r 640x480 $path"1.jpg"
rm -f $path"1.jpg"
sleep 1
fswebcam --no-banner -r 640x480 $path"2.jpg"
rm -f $path"2.jpg"
sleep 1

fswebcam --no-banner -r 640x480 $path".jpg"

python3 ./monitor.py $path".jpg" $last_file

