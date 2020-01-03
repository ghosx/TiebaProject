#!/usr/bin/env bash
echo "开始一键安装"
echo "大约需要一个小时"
cd /root
wget http://soft.vpser.net/lnmp/lnmp1.6.tar.gz -cO lnmp1.6.tar.gz && tar zxf lnmp1.6.tar.gz && cd lnmp1.6 && LNMP_Auto="y" DBSelect="3" DB_Root_Password="sign.heeeepin.com" InstallInnodb="y" PHPSelect="7" SelectMalloc="1" CheckMirror="n" ./install.sh lnmp
cd /home/wwwroot
wget https://github.com/ghosx/TiebaProject/archive/V3.0.tar.gz
tar xvf V3.0.tar.gz
mv TiebaProject-3.0/ tiebaProject
chmod 777 -R tiebaProject
cd tiebaProject
mkdir logs
apt install python3-pip -y
pip3 install -r requirements.txt
mysql -uroot -psign.heeeepin.com -e "CREATE DATABASE tiebaproject default charset utf8 collate utf8_general_ci;"
mysql -uroot -psign.heeeepin.com -e "exit;"
python3 manage.py makemigrations
python3 manage.py migrate
pip3 install uwsgi
echo '[uwsgi]
master = true
processes = 1
threads = 2
chdir = /home/wwwroot/tiebaProject
module = tiebaProject.wsgi
socket= 0.0.0.0:9000
logto = /home/wwwroot/tiebaProject/logs/error.log
pidfile = /home/wwwroot/tiebaProject/uwsgi.pid
chmod-socket = 664
vacuum = true
master = true
max-requests = 1000' > /home/wwwroot/tiebaProject/uwsgi.ini

nohup uwsgi --ini uwsgi.ini &

cd /usr/local/nginx/conf
mv nginx.conf nginx.conf.back
echo "user  www www;

worker_processes auto;
worker_cpu_affinity auto;

error_log  /home/wwwlogs/nginx_error.log  crit;

pid        /usr/local/nginx/logs/nginx.pid;
#Specifies the value for maximum file descriptors that can be opened by this process.
worker_rlimit_nofile 51200;
events
    {
        use epoll;
        worker_connections 51200;
        multi_accept off;
        accept_mutex off;
    }
http
    {
        include       mime.types;
        default_type  application/octet-stream;

        server_names_hash_bucket_size 128;
        client_header_buffer_size 32k;
        large_client_header_buffers 4 32k;
        client_max_body_size 50m;
        sendfile on;
        sendfile_max_chunk 512k;
        tcp_nopush on;
        keepalive_timeout 60;
        tcp_nodelay on;
        fastcgi_connect_timeout 300;
        fastcgi_send_timeout 300;
        fastcgi_read_timeout 300;
        fastcgi_buffer_size 64k;
        fastcgi_buffers 4 64k;
        fastcgi_busy_buffers_size 128k;
        fastcgi_temp_file_write_size 256k;
        gzip on;
        gzip_min_length  1k;
        gzip_buffers     4 16k;
        gzip_http_version 1.1;
        gzip_comp_level 2;
        gzip_types     text/plain application/javascript application/x-javascript text/javascript text/css application/xml application/xml+rss;
        gzip_vary on;
        gzip_proxied   expired no-cache no-store private auth;
        server_tokens off;
        access_log off;

server {
    listen         80;
    server_name    0.0.0.0;
     proxy_connect_timeout    600;
proxy_read_timeout       600;
proxy_send_timeout       600;
    charset UTF-8;
    access_log      /home/wwwroot/tiebaProject/access_log;
    error_log       /home/wwwroot/tiebaProject/error_log;

    client_max_body_size 75M;

    location / {
        include uwsgi_params;
        uwsgi_pass 0.0.0.0:9000;
    }
    location /static {
        alias /home/wwwroot/tiebaProject/static;
     }
 }

include vhost/*.conf;
}" > nginx.conf
nginx -s reload
service nginx restart
cd /home/wwwroot/tiebaProject

apt install expect -y

expect -c "
spawn python3 manage.py createsuperuser
expect {
    \"Username*\" {set timeout 300; send \"admin\r\";exp_continue;}
    \"Email address*\" {send \"admin@qq.com\r\";exp_continue;}
    \"Password*\" {send \"admin123456\r\";exp_continue;}
    \"Password*\" {send \"admin123456\r\"; }
      }"

nohup python3 task.py &
# 定时任务
echo "# 每分钟判断一次进程是否异常退出，实现自动重启
*/1 * * * * /bin/bash /www/wwwroot/tiebaProject/restart.sh > /dev/null
# 晚上23：50进行日志分割，防止占用大量磁盘空间
50 23 * * * /bin/bash /www/wwwroot/tiebaProject/process_log.sh > /dev/null
# 晚上23：30杀死进程并且重启，防止进程僵死
30 23 * * * /bin/bash /www/wwwroot/tiebaProject/kill.sh > /dev/null" >> /var/spool/cron/root
echo "安装完毕"
echo "打开http://你的ip 开始享受吧"
echo "后台管理地址 http://你的ip/admin/  用户名 admin 密码 admin123456"




