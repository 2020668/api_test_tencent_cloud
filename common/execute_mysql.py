# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/15

E-mail:keen2020@outlook.com

=================================


"""

import pymysql
from common.config import conf


class ExecuteMysql(object):

    def __init__(self):

        # 连接数据库
        self.con = pymysql.connect(
            host=conf.get("mysql", "host"),
            port=conf.getint("mysql", "port"),
            user=conf.get("mysql", 'user'),
            password=conf.get("mysql", "password"),
            database=conf.get("mysql", "database"),
            charset="utf8")
        # 创建游标
        self.cur = self.con.cursor()

    def find_one(self, sql):

        # 执行sql语句
        self.cur.execute(sql)
        # 刷新数据，并返回查询结果
        self.con.commit()
        return self.cur.fetchone()

    def find_many(self, sql, number):

        # 执行sql语句
        self.cur.execute(sql)
        # 刷新数据，并返回查询结果
        self.con.commit()
        return self.cur.fetchmany(number)

    def find_all(self, sql):

        # 执行sql语句
        self.cur.execute(sql)
        # 刷新数据，并返回查询结果
        self.con.commit()
        return self.cur.fetchall()

    def find_count(self, sql):
        count = self.cur.execute(sql)
        self.con.commit()
        return count

    def close(self):
        self.con.close()


if __name__ == '__main__':

    db = ExecuteMysql()
    phone = '18825046772'
    a = db.find_count("select id from member where mobilephone={}".format(phone))
    print(a)
