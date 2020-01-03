#!/usr/bin/env bash
#/bin/bash
# author: ghosx
# date: 2019/12/12
# desc: this script is used to kill the process of task.py and it's threed
ps -ef |grep 'python3 task.py' |grep -v grep > /dev/null
if [ $? -eq 0 ]
then
    ps -ef |grep 'python3 task.py' |grep -v grep | awk '{printf $2}' | xargs kill -9
    echo 'success to kill the task'
else
    echo 'no such process of thr task.py'
fi
