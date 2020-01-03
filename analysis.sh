#!/usr/bin/env bash
# 这个脚本是用来统计有多少人自己搭建了签到网站
cd /www/wwwlogs
cat heeeepin.com.log | awk '$7 == "/1.js" {printf $1 " " $11 "\n"}'|uniq