#!/bin/bash

startTime=`date +%Y%m%d-%H:%M`

startTime_s=`date +%s`

echo "   "
echo "******************Start running GPUMD tasks********************"
echo "   "

export CUDA_VISIBLE_DEVICES=1

/home/liangt/software/GPUMD/GPUMD-15-09-2024-3.9.3/src/gpumd

nvidia-smi

endTime=`date +%Y%m%d-%H:%M`

endTime_s=`date +%s`

sumTime=$[$endTime_s - $startTime_s]

Hour=$[sumTime/3600]

echo "   "
echo "******************End running GPUMD tasks********************"
echo "   "

echo "$startTime ---> $endTime" "Total:$Hour  hours"

# Sent email to liangting.zj@gmail.com
# https://blog.csdn.net/qq_20732247/article/details/107089175
# liang:18077330128@163.com:smtp.163.com:465

#echo "***** The GPUMD job already DONE !!! Submit another !!! ***" | mail -s "JOB Finish Normally" liangting.zj@gmail.com
