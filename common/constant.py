# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/6

E-mail:keen2020@outlook.com

=================================


"""


import os


"""
封装动态获取常量，项目中使用的各种绝对路径
"""

# 获取项目目录的根路径
BASE_DIR = os.path.dirname(os.path.dirname(__file__))   # 二级目录是common，一级目录（根目录)就是qcd_api_test

# 获取配置文件目录的路径
CONF_DIR = os.path.join(BASE_DIR, 'conf')

# 获取excel数据目录的路径
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 获取日志目录的路径
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# 获取报告目录的路径
REPORT_DIR = os.path.join(BASE_DIR, 'report')

# 获取测试用例目录的路径
CASE_DIR = os.path.join(BASE_DIR, 'testcases')
