# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/25

E-mail:keen2020@outlook.com

=================================


"""

import re
from common.config import conf
import random
from common.execute_mysql import ExecuteMysql

# 匹配两个#中间的任意字符，至少一次，关闭贪婪
p = r"#(.+?)#"
db = ExecuteMysql()


class ConText(object):
    pass


# def read(data):
#     setattr(ConText, "key", data)

# 接收号段，然后随机生成8位0-9的数字，添加在号段后面，组合成为指定号段的随机号码
def rand_phone(segment):
    phone = str(segment)
    for i in range(8):
        phone_end = random.randint(0, 9)
        phone += str(phone_end)
    return phone


# 对测试用例的参数数据进行处理
def data_replace(data):
    """
    :param data: 用例的参数
    :return: 替换之后的结果
    """

    # 提取请求数据#中间的字符, 当请求参数有#时才执行下方代码，替换完成后使用相同的变量名,再次做出判断,即可退出循环

    while re.search(p, data):
        key = re.search(p, data).group(1)
        try:
            value = conf.get("test_data", key)      # 与配置文件匹配
        except:
            if "loanid" in data:
                value = getattr(ConText, "loanid")      # 提供Content类,可以先设置属性再来获取
            elif "phone1" in data:
                while True:
                    value = rand_phone(eval(data)["mobilephone"][6:9])  # 获取请求数据的mobilephone后面的手机号段,组合成随机号码
                    # 查询数据库有无该随机号码
                    count = db.find_count("SELECT Id FROM member WHERE MobilePhone={}".format(value))

                    print(count)

                    # 数据库中无此随机号码，就不用继续随机生成，直接使用该随机号码
                    if count == 0:
                        break
            else:
                return "请求参数有误"
        data = re.sub(p, value, data, count=1)    # 将data的#号之间的数字，用value进行替换，替换成功后没有#就退出循环
    return data


# 获取随机的用户名，由6位包括数字，大写，小写字母组成
def rand_name():
    name = ""
    for i in range(6):
        num = random.randint(0, 9)
        # num = chr(random.randint(48,57))  # ASCII表示数字
        letter = chr(random.randint(97, 122))   # 取小写字母
        Letter = chr(random.randint(65, 90))    # 取大写字母
        s = str(random.choice([num, letter, Letter]))
        name += s
    return name


# 生成随机的ip地址
def rand_ip():
    ip = '{}.{}.{}.{}'.format(random.randint(0, 255), random.randint(0, 255),
                              random.randint(0, 255), random.randint(0, 255))
    return ip


if __name__ == '__main__':
    # data = "#phone150#shg;g#pwd#"

    data = '{"mobilephone":"#login_phone1#", "pwd":"#pwd1#"}'

    # data = "{'mobilephone':'#phone155#', 'pwd':'abc123456', 'regname':'张三'}"
    # res = data_replace(data)
    data = '{"mobilephone":"13333113752", "pwd":"#pwd3#"}'

    res = data_replace(data)
    print(res)
