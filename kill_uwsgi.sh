#/bin/bash
# author: ghosx
# date: 2019/12/12
# desc: this script is used to kill the process of task.py and it's threed
cat uwsgi.pid | xargs kill -9
echo 'success to kill the uwsgi'
