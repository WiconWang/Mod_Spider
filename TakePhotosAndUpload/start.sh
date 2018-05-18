#!/bin/bash
nowtime=`date +%Y%m%d_%H%M%S`
path="~/Monitor/Cam_$nowtime.jpg"
fswebcam --no-banner -r 640x480 $path
/usr/bin/python processer.py  $path
