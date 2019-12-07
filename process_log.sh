#!/bin/bash
# Author: ghosx
# Last Update: 2019.12.07
# Description: task.log 日志分割
 
this_path=$(cd `dirname $0`;pwd)   #根据脚本所在路径
current_date=`date -d "-1 day" "+%Y%m%d"`   #列出时间
cd $this_path
echo $this_path
echo $current_date 
 
do_split () {
    [ ! -d logs ] && mkdir -p logs
    split -b 10m -d -a 4 ./task.log   ./logs/task-${current_date}  #切分10兆每块至logs文件中，格式为：nohup-xxxxxxxxxx
    if [ $? -eq 0 ];then
        echo "Split is finished!"
    else
        echo "Split is Failed!"
        exit 1
    fi
}
 
do_del_log() {
    find ./logs -type f -ctime +3 | xargs rm -rf #清理3天前创建的日志
    cat /dev/null > task.log  #清空当前目录的task.log文件
}
 
if do_split ;then
    do_del_log
    echo "nohup is split Success"
else
    echo "nohup is split Failure"
    exit 2
fi
[root@VM_176_212_centos TiebaProject]# a = `date "+%Y-%m-%d"`
-bash: a: command not found
[root@VM_176_212_centos TiebaProject]# var a = `date "+%Y-%m-%d"`
-bash: var: command not found
[root@VM_176_212_centos TiebaProject]# var a
-bash: var: command not found
[root@VM_176_212_centos TiebaProject]# let a
[root@VM_176_212_centos TiebaProject]# a = `date "+%Y-%m-%d"`
-bash: a: command not found
[root@VM_176_212_centos TiebaProject]# a=`date "+%Y-%m-%d"`
[root@VM_176_212_centos TiebaProject]# echo $a
2019-12-07
[root@VM_176_212_centos TiebaProject]# a=`date "+%Y_%m_%d"`
[root@VM_176_212_centos TiebaProject]# echo $a
2019_12_07
[root@VM_176_212_centos TiebaProject]# vim process_log.sh 
[root@VM_176_212_centos TiebaProject]# 
[root@VM_176_212_centos TiebaProject]# 
[root@VM_176_212_centos TiebaProject]# 
[root@VM_176_212_centos TiebaProject]# crontab -e
crontab: installing new crontab
[root@VM_176_212_centos TiebaProject]# 
[root@VM_176_212_centos TiebaProject]# 
[root@VM_176_212_centos TiebaProject]# 
[root@VM_176_212_centos TiebaProject]# 
[root@VM_176_212_centos TiebaProject]# 
[root@VM_176_212_centos TiebaProject]# 
[root@VM_176_212_centos TiebaProject]# 
[root@VM_176_212_centos TiebaProject]# 
[root@VM_176_212_centos TiebaProject]# ./process_log.sh 
/www/wwwroot/TiebaProject
2019_12_07
Split is finished!
nohup is split Success
[root@VM_176_212_centos TiebaProject]# ls logs/
task-201912060000  task-201912060009  task-201912060018  task-201912060027  task-201912060036  task-201912060045  task-201912060054    task-2019_12_070006
task-201912060001  task-201912060010  task-201912060019  task-201912060028  task-201912060037  task-201912060046  task-201912060055    task-2019_12_070007
task-201912060002  task-201912060011  task-201912060020  task-201912060029  task-201912060038  task-201912060047  task-201912060056    task-2019_12_070008
task-201912060003  task-201912060012  task-201912060021  task-201912060030  task-201912060039  task-201912060048  task-2019_12_070000  task-2019_12_070009
task-201912060004  task-201912060013  task-201912060022  task-201912060031  task-201912060040  task-201912060049  task-2019_12_070001  task-2019_12_070010
task-201912060005  task-201912060014  task-201912060023  task-201912060032  task-201912060041  task-201912060050  task-2019_12_070002
task-201912060006  task-201912060015  task-201912060024  task-201912060033  task-201912060042  task-201912060051  task-2019_12_070003
task-201912060007  task-201912060016  task-201912060025  task-201912060034  task-201912060043  task-201912060052  task-2019_12_070004
task-201912060008  task-201912060017  task-201912060026  task-201912060035  task-201912060044  task-201912060053  task-2019_12_070005
[root@VM_176_212_centos TiebaProject]# rm logs/* -y
rm: invalid option -- 'y'
Try 'rm --help' for more information.
[root@VM_176_212_centos TiebaProject]# rm -y logs/*
rm: invalid option -- 'y'
Try 'rm --help' for more information.
[root@VM_176_212_centos TiebaProject]# rm -f logs/*
[root@VM_176_212_centos TiebaProject]# ls
app.log       LICENSE  manage.py  process_log.sh  README.md         restart.sh  static    task.py       tiebaproject_venv
constants.py  logs     nohup.out  __pycache__     requirements.txt  SignIn      task.log  TiebaProject  uwsgi.ini
[root@VM_176_212_centos TiebaProject]# ./process_log.sh 
/www/wwwroot/TiebaProject
2019_12_07
Split is finished!
nohup is split Success
[root@VM_176_212_centos TiebaProject]# ls logs/
[root@VM_176_212_centos TiebaProject]# ls logs/
[root@VM_176_212_centos TiebaProject]# cat process_log.sh 
#!/bin/bash
# Author: ghosx
# Last Update: 2019.12.07
# Description: task.log 日志分割
 
this_path=$(cd `dirname $0`;pwd)   #根据脚本所在路径
current_date=`date "+%Y_%m_%d"`   #列出时间
cd $this_path
echo $this_path
echo $current_date 
 
do_split () {
    [ ! -d logs ] && mkdir -p logs
    split -b 10m -d -a 4 ./task.log   ./logs/task-${current_date}  #切分10兆每块至logs文件中，格式为：nohup-xxxxxxxxxx
    if [ $? -eq 0 ];then
        echo "Split is finished!"
    else
        echo "Split is Failed!"
        exit 1
    fi
}
 
do_del_log() {
    find ./logs -type f -ctime +3 | xargs rm -rf #清理3天前创建的日志
    cat /dev/null > task.log  #清空当前目录的task.log文件
}
 
if do_split ;then
    do_del_log
    echo "nohup is split Success"
else
    echo "nohup is split Failure"
    exit 2
fi
