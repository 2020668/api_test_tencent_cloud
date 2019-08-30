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
    while re.search(p, data):
        key = re.search(p, data).group(1)
        try:
            value = conf.get("test_data", key)
        except:
            # value = getattr(ConText, "loanid")
            if "loanid" in data:
                value = getattr(ConText, "loanid")
            elif "phone1" in data:
                value = rand_phone(eval(data)["mobilephone"][6:9])   # 获取请求数据的mobilephone后面的手机号段,组合成随机号码
                while True:
                    value1 = "15517970510"
                    # 查询数据库有无该随机号码
                    count = db.find_count("SELECT Id FROM member WHERE MobilePhone={}".format(value1))
                    # 数据库中无此随机号码，就不用继续随机生成，直接使用该随机号码
                    if count == 0:
                        break
        data = re.sub(p, value1, data, count=1)    # 将data的#号之间的数字，用value进行替换
    return data


# 获取随机的用户名，由6位包括数字，大写，小写字母组成
def rand_name():
    ret = ""
    for i in range(6):
        num = random.randint(0, 9)
        # num = chr(random.randint(48,57))  # ASCII表示数字
        letter = chr(random.randint(97, 122))   # 取小写字母
        Letter = chr(random.randint(65, 90))    # 取大写字母
        s = str(random.choice([num, letter, Letter]))
        ret += s
    return ret


# 生成随机的ip地址
def rand_ip():
    ip = '{}.{}.{}.{}'.format(random.randint(0, 255), random.randint(0, 255),
                              random.randint(0, 255), random.randint(0, 255))
    return ip


if __name__ == '__main__':
    # data = "#phone150#shg;g#pwd#"
    data = "{'mobilephone':'#phone155#', 'pwd':'abc123456', 'regname':'张三'}"
    res = data_replace(data)
    print(res)
