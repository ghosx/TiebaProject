#!/usr/bin/env bash

# 配合 crontab 即可做到task.py出错自动恢复
# */1 * * * * /bin/bash /www/wwwroot/TiebaProject/restart.sh

ps -ef |grep 'pypy3 task.py' |grep -v grep > /dev/null
if [ $? -ne 0 ]
then
    echo 'task.py is not running...'
    echo 'try to restart task.py'
    cd /home/wwwroot/tiebaProject
    nohup pypy3 task.py > /dev/null &
else
    echo "Main is running"
fi

