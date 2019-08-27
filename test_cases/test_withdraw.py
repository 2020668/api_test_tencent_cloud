# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/15

E-mail:keen2020@outlook.com

=================================


"""

import unittest
from library.ddt import ddt, data
from common.read_excel import ReadExcel
from common.logger import my_log   # 可直接导入对象
from common.config import conf
import os
from common.constant import DATA_DIR
from common.http_request import HTTPRequest2
from common.execute_mysql import ExecuteMysql
from common.tools import rand_phone
from common.tools import data_replace
from decimal import Decimal


# 从配置文件获取数据
file_name = conf.get('excel', 'file_name')
read_column = conf.get('excel', 'read_column')
read_column = eval(read_column)     # 将str转换成list


@ddt
class WithdrawTestCase(unittest.TestCase):

    # 拼接完整的excel路径，然后读取excel数据
    wb = ReadExcel(os.path.join(DATA_DIR, file_name), "withdraw")
    cases = wb.read_column_data(read_column)

    @classmethod
    def setUpClass(cls):
        my_log.info("======== 准备开始执行取现接口的测试 ========")
        cls.request = HTTPRequest2()
        cls.db = ExecuteMysql()

    @classmethod
    def tearDownClass(cls):
        my_log.info("======== 取现接口测试执行完毕 ========")
        cls.request.close()
        cls.db.close()

    @data(*cases)   # 拆包，拆成几个参数
    def test_withdraw(self, case):
        # 筛选用例的请求数据中做了#register__phone#标记的数据
        if "#register_phone#" in case.request_data:
            while True:
                # 生成随机号码
                mobile_phone = rand_phone()
                # 查询数据库有无该随机号码
                count = self.db.find_count("SELECT Id FROM member WHERE MobilePhone={}".format(mobile_phone))
                # 数据库中无此随机号码，就不用继续随机生成，直接使用该随机号码
                if count == 0:
                    break
            # 将用例中的#register__phone#替换成随机生成的手机号码
            case.request_data = case.request_data.replace("#register_phone#", mobile_phone)

        # 选取请求的电话号为已注册的测试用例数据
        if "#exists_phone#" in case.request_data:
            # 从数据库获取第一条号码，给用例参数
            mobile_phone = self.db.find_one("SELECT MobilePhone FROM member LIMIT 1")[0]
            # 用从数据库获取的号码替换掉请求数据中的标记#exists_phone
            case.request_data = case.request_data.replace("#exists_phone#", mobile_phone)

        case.request_data = data_replace(case.request_data)

        # 判断是否需要校验数据库
        if case.check_mysql:
            # 将登录手机号替换掉sql语句中的标记#login_phone#
            case.check_mysql = data_replace(case.check_mysql)
            # 调用查询数据方法，传入sql语句，返回元组，下标0取值，decimal
            before_money = self.db.find_one(case.check_mysql)[0]

        # 拼接url地址，发送请求
        url = conf.get("env", "url") + case.url
        self.row = case.case_id + 1
        response = self.request.request(method=case.method, url=url, data=eval(case.request_data))  # 将str转换成dict
        # 该打印的内容会显示在报告中
        print("请求数据--> {}".format(case.request_data))
        print("期望结果---> {}".format(case.expected_data))
        print("服务器响应数据--> {}".format(response.json()))

        # res = response.json()返回json格式，自动转换成Python的dict类型，只取部分字段进行断言
        res = {"status": response.json()["status"], "code": response.json()["code"], "msg": response.json()["msg"]}

        try:
            self.assertEqual(eval(case.expected_data), res)

            if case.check_mysql:
                # case.request_data是str类型，先转换为dict再来取值,float
                money = eval(case.request_data)["amount"]
                # 将float类型转换成decimal类型，与数据库查询的结果数据类型一致，并设置保留2位小数
                money = Decimal.from_float(money).quantize(Decimal("0.00"))
                after_money = self.db.find_one(case.check_mysql)[0]
            if "取现成功" in response.json()["msg"]:
                # 该打印的内容会显示在报告中
                print("取现前余额为:{}, 本次取现:{}, 取现后余额:{}".format(before_money, money, after_money))
                self.assertEqual(before_money - money, after_money)

        except AssertionError as e:
            result = 'FAIL'
            my_log.exception(e)     # 将异常信息记录到日志
            raise e
        else:
            result = 'PASS'
            my_log.debug("预期结果：%s, 实际结果：%s, 测试通过" % (eval(case.expected_data), res))

        finally:
            self.wb.write_data(row=self.row, column=10, value=str(res))
            self.wb.write_data(row=self.row, column=11, value=result)

