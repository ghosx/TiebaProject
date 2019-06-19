# 贴吧云签到云回复

## 项目简介

独立开发的基于Django的贴吧云签到云回网站

作者维护的地址：http://sign.heeeepin.com/
## 如何使用
### 项目环境
Linux / macOS

MySQL / MariaDB

Windows暂不兼容（无法执行Cron）


### 项目安装
本地安装演示视频

https://www.bilibili.com/video/av55931920/

## 初始化数据库
参考 https://www.centos.bz/2018/07/centoslinux-%E4%B8%8Bmysql8-0-11%E7%9A%84%E5%AE%89%E8%A3%85/
```shell
sudo service mysql start
```
或
```shell
sudo systemctl enable mysql && sudo systemctl start mysql
```
授予权限（本地安装用）
```shell
mysql -u root -p
mysql> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
mysql> flush privileges;
```
创建tieba数据库
```shell
mysql> CREATE DATABASE tieba;
```
## 初始化
克隆代码（或手动下载）
```shell
git clone https://github.com/ghosx/TiebaProject.git
```
修改`settings.py` 中的数据库配置
```
cd TiebaProject
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py data
```
### 添加定时任务
```shell
python3 manage.py crontab add
```
### 项目启动
```shell
python3 manage.py runserver 0.0.0.0:8000
```
执行完上述命令后访问 [http://127.0.0.1:8000/](http://127.0.0.1:8000/) 即可

### 常驻后台（本地安装用）
```shell
nohup python3 manage.py runserver 0.0.0.0:8000 &
```

## 项目首页
![ha.gif](https://i.loli.net/2018/08/16/5b7556bb2ce4e.png)

## emmmm.... 

求 **Star** 求 **Follow**

## 讨论群

TG： https://t.me/tiebasign

qq群： 818794879

## LICENSE

[WTFPL – Do What the Fuck You Want to Public License](http://www.wtfpl.net/about/)
