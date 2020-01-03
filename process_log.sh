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
