# 使用docker仓库中的基础nginx镜像
FROM nginx
# 开放端口
EXPOSE 80 8000
# 删除nginx原有配置文件
RUN rm /etc/nginx/conf.d/default.conf
# 将自己写的配置文件添加到容器
ADD nginx.conf /etc/nginx/conf.d/
# 创建web应用的静态文件存储
RUN mkdir -p /usr/share/nginx/html/static
# 创建存放日志的文件夹
RUN mkdir -p /home/logs