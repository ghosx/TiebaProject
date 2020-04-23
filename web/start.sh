#!/bin/bash
# 等待mysql服务启动
echo "等待mysql服务启动"
sleep 10
# 迁移django数据库
echo "迁移django数据库"
python manage.py migrate
# 导入数据
echo "导入数据"
python manage.py loaddata initial_data.yaml
# 启动后台任务
echo "启动supervisord任务"
supervisord -c supervisord.conf
# 启动web服务
echo "启动web服务"
python /app/manage.py runserver 0.0.0.0:8000


