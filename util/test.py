# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/21

E-mail:keen2020@outlook.com

=================================


"""

import re

re_qq = ''
str_re1 = r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
str_re2 = r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$'
str_re3 = r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$'


# def check_email(email):
#     # reg = r'^[\w]{1,19}@((163)|(qq)|(126)).((com)|(cn))$'
#     p = re.compile(str_re3)
#     if p.match(email):
#         print('{}, 邮箱有效'.format(email))
#     else:
#         print({}, '邮箱无效'.format(email))
#
#
# # email = "lilei1880@QQ.COM"
# while True:
#     email = input("请输入邮箱地址：")
#     check_email(email)


re_test = r'*+@*+.$'
res = re.findall(re_test, '115448855@qq.com')
print(res)
