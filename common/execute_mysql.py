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

    # 查询一条结果 没有返回None 有多条数据只返回第一条数据
    def find_one(self, sql):

        # 执行sql语句
        self.cur.execute(sql)
        # 刷新数据，并返回查询结果
        self.con.commit()
        return self.cur.fetchone()

    # 传入数字 查询符合条件的结果 从前往后 只取指定数字个数的结果  没有返回空元组
    def find_many(self, sql, number):

        # 执行sql语句
        self.cur.execute(sql)
        # 刷新数据，并返回查询结果
        self.con.commit()
        return self.cur.fetchmany(number)

    # 查询符合条件的所有结果 没有返回空元组
    def find_all(self, sql):

        # 执行sql语句
        self.cur.execute(sql)
        # 刷新数据，并返回查询结果
        self.con.commit()
        return self.cur.fetchall()

    # 查询个数 没有返回0
    def find_count(self, sql):
        count = self.cur.execute(sql)
        self.con.commit()
        return count

    # 断开数据库连接
    def close(self):
        self.con.close()


if __name__ == '__main__':

    db = ExecuteMysql()
    phone = '18834934510'
    # 查询个数 只有1个
    a = db.find_count("select Id from member where mobilephone={}".format(phone))
    print(a)

    # 查询一条结果 没有返回None
    b = db.find_one("select Id from member where mobilephone={}".format(phone))
    # 返回结果是一个元组 使用[0]获取值
    print(b)

    # 查询指定数量的结果 没有返回空元组
    c = db.find_many("select * from member where Id > 1270", 2)
    print(c)

    # 查询全部结果 没有返回空元组
    d = db.find_all("select * from member where Id > 1270")
    print(d)
