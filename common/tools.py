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

# 匹配两个#中间的任意字符，至少一次，关闭贪婪
p = r"#(.+?)#"


class ConText(object):
    pass


# def read(data):
#     setattr(ConText, "key", data)


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
        data = re.sub(p, value, data, count=1)
    return data


def rand_phone():
    phone = "133"
    for i in range(8):
        phone_end = random.randint(0, 9)
        phone += str(phone_end)
    return phone


if __name__ == '__main__':
    data = "hasdgiioghgaoigh#login_phone1#shg;g#pwd#"
    res = data_replace(data)
    print(res)
