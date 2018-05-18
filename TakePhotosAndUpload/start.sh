#!/bin/bash
nowtime=`date +%Y%m%d_%H%M%S`
path="/home/pi/Monitor/Cam_$nowtime.jpg"
fswebcam --no-banner -r 640x480 $path
python3 processer.py  $path
