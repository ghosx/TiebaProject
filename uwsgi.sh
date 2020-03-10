#/bin/bash
# author: ghosx
# date: 2019/12/12
cd /home/wwwroot/tiebaProject
nohup uwsgi uwsgi.ini > /dev/null &

