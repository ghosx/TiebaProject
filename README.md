# 贴吧云签到云回复

## 项目简介

独立开发的基于Django的贴吧云签到云回网站
作者维护的地址：http://sign.heeeepin.com/
## 如何使用
### 项目安装
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

## 项目首页
![ha.gif](https://i.loli.net/2018/08/16/5b7556bb2ce4e.png)

## emmmm.... 

求 **Star** 求 **Follow**

## 讨论群

TG： https://t.me/tiebasign

qq群： 818794879

## LICENSE

[WTFPL – Do What the Fuck You Want to Public License](http://www.wtfpl.net/about/)

