# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/21

E-mail:keen2020@outlook.com

=================================


"""

import random

mobilephone = "133"
for i in range(8):
    mobilephone_end = random.randint(0, 9)
    mobilephone += str(mobilephone_end)

print(mobilephone)
