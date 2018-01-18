#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@TIME   :2018/1/16 16:08
import mysql.connector

MYSQL_HOSTS='127.0.0.1'
MYSQL_USER='root'
MYSQL_PASSWORD='root'
MYSQL_PORT='3306'
MYSQL_DB='tiku'
conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB,host=MYSQL_HOSTS)
cursor = conn.cursor(buffered=True)

class Sql:
    @classmethod
    def insert_shiti(cls,id,sort_id,answer):
        cursor.execute('insert shiti values(%s,%s,%s)',[id,sort_id,answer])
        if cursor.rowcount:
            conn.commit()
            print('试题保存成功')
            return True
        else:
            conn.rollback()
            print('试题保存失败')
            return False

    @classmethod
    def select_id(cls,id,answer):
        cursor.execute('SELECT EXISTS (select 1 from shiti where id=%s and answer=%s)',[id,answer])
        # 如果存在则会返回 1 不存在则会返回0
        result = cursor.fetchall()[0]
        return result