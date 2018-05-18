#!/bin/bash
nowtime=`date +%Y%m%d_%H%M%S`
path="/home/pi/Monitor/Cam_$nowtime"
fswebcam --no-banner -r 640x480 $path"1.jpg"
#USB摄像头第一张一般都不清晰，所以一秒后再拍一张
sleep 1
fswebcam --no-banner -r 640x480 $path".jpg"
python3 processer.py $path+".jpg"
rm -f $path"1.jpg"
