# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/4

E-mail:keen2020@outlook.com

=================================


"""

import unittest
from library.HTMLTestRunnerNew import HTMLTestRunner
from common.config import conf
from common.constant import CASE_DIR, REPORT_DIR
from common.send_email import SendEmail
import os
import time


_title = conf.get('report', 'title')
_description = conf.get('report', 'description')
_tester = conf.get('report', 'tester')
report_name = conf.get('report', 'report_name')
report_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + "_" + report_name
mail_title = conf.get('mail', 'mail_title')
mail_message = conf.get('mail', 'mail_message')
file_path = os.path.join(REPORT_DIR, report_name)

suite = unittest.TestSuite()  # 创建测试集合
loader = unittest.TestLoader()
suite.addTest(loader.discover(CASE_DIR))

with open(file_path, 'wb') as f:
    runner = HTMLTestRunner(
        stream=f,
        verbosity=2,
        title=_title,
        description=_description,
        tester=_tester
    )
    runner.run(suite)


# 发送email
# SendEmail.send_qq_file_mail(mail_title, mail_message, file_path)
# SendEmail.send_outlook_file_mail(mail_title, mail_message, file_path)

