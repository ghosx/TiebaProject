#!/usr/bin/env bash
echo "开始一键安装"
echo "大约需要一个小时"
cd /root
wget http://soft.vpser.net/lnmp/lnmp1.6.tar.gz -cO lnmp1.6.tar.gz && tar zxf lnmp1.6.tar.gz && cd lnmp1.6 && LNMP_Auto="y" DBSelect="3" DB_Root_Password="sign.heeeepin.com" InstallInnodb="y" PHPSelect="7" SelectMalloc="1" CheckMirror="n" ./install.sh lnmp
cd /home/wwwroot
wget https://github.com/ghosx/TiebaProject/archive/V2.0.tar.gz
tar xvf V2.0.tar.gz
mv TiebaProject-2.0/ TiebaProject
chmod 777 -R TiebaProject
cd TiebaProject
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
chdir = /home/wwwroot/TiebaProject
module = TiebaProject.wsgi
socket= 0.0.0.0:9000
logto = /home/wwwroot/TiebaProject/logs/error.log
pidfile = /home/wwwroot/TiebaProject/uwsgi.pid
chmod-socket = 664
vacuum = true
master = true
max-requests = 1000' > /home/wwwroot/TiebaProject/uwsgi.ini

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
    access_log      /home/wwwroot/TiebaProject/access_log;
    error_log       /home/wwwroot/TiebaProject/error_log;

    client_max_body_size 75M;

    location / {
        include uwsgi_params;
        uwsgi_pass 0.0.0.0:9000;
    }
    location /static {
        alias /home/wwwroot/TiebaProject/static;
     }
 }

include vhost/*.conf;
}" > nginx.conf
nginx -s reload
service nginx restart
cd /home/wwwroot/TiebaProject
python3 manage.py createsuperuser --username admin --email admin@qq.com
admin123456
admin123456
nohup python3 task.py &
echo "安装完毕"
echo "打开http://你的ip 开始享受吧"
echo "后台管理地址 http://你的ip/admin/  用户名 admin 密码 admin123456"




