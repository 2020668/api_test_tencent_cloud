# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2020/2/29

E-mail:keen2020@outlook.com

=================================


"""


ls1 = [1, 2, 3]
ls2 = [4, 5, 6]
a = ls1.extend(ls2)
# print(a)
# print(ls1)
# # del ls1[1]
# print(ls1)
#
# a = (1)
# print(a)
# print(type(a))

while True:
    score = eval(input("请输入分数:"))
    if type(score) not in (str, int):
        print("你的输入有误，请重新输入！")
    elif score >= 90:
        print("分数为:{}, 成绩非常优秀!".format(score))
    elif score >= 80:
        print("分数为:{}, 成绩优秀!".format(score))
    elif score >= 70:
        print("分数为:{}, 成绩良好!".format(score))
    elif score >= 60:
        print("分数为:{}, 成绩及格!".format(score))
    else:
        print("分数为:{}, 成绩不及格!".format(score))

