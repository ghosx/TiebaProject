# 使用docker仓库中的基础nginx镜像
FROM mysql:5.6
# 使用自定义的mysqld.cnf
RUN rm /etc/mysql/mysql.conf.d/mysqld.cnf
ADD mysqld.cnf /etc/mysql/mysql.conf.d/
