#!/bin/sh

# 启动 MySQL 服务
/usr/bin/mysqld_safe --datadir='/var/lib/mysql' &

# 等待 MySQL 服务启动
while ! mysqladmin ping --silent; do
    echo "等待 MySQL 启动..."
    sleep 1
done

# 初始化数据库
if [ -f /app/init_db.sql ]; then
    echo "初始化数据库..."
    mysql -u root < /wk/mysql/init_db.sql
fi

# 启动 Python 服务
python3 /wk/app/web_nav.py
