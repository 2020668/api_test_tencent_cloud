# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/24

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
from common.tools import data_replace
from common.tools import ConText
from decimal import Decimal


# 从配置文件获取数据
file_name = conf.get('excel', 'file_name')
read_column = conf.get('excel', 'read_column')
read_column = eval(read_column)     # 将str转换成list


@ddt
class BidLoanTestCase(unittest.TestCase):

    # 拼接完整的excel路径，然后读取excel数据
    wb = ReadExcel(os.path.join(DATA_DIR, file_name), "bidLoan")
    cases = wb.read_column_data(read_column)

    @classmethod
    def setUpClass(cls):

        my_log.info("准备开始执行投资接口的测试......")
        cls.request = HTTPRequest2()
        cls.db = ExecuteMysql()

    @data(*cases)   # 拆包，拆成几个参数
    def test_bid_loan(self, case):

        if case.check_mysql:
            if "投资" in case.title:
                case.check_mysql = data_replace(case.check_mysql)
                before_money = self.db.find_one(case.check_mysql)[0]

        if "#nomemberid#" in case.request_data:
            memberid = self.db.find_one("SELECT MAX(Id) FROM member")[0] + 1
            case.request_data = case.request_data.replace("#nomemberid#", str(memberid))

        if "#noloanid#" in case.request_data:
            loanid = self.db.find_one("SELECT MAX(Id) FROM loan")[0] + 1
            case.request_data = case.request_data.replace("#noloanid#", str(loanid))

        # 先替换有特殊字段和sql语句的，再来替换一般用例
        case.request_data = data_replace(case.request_data)

        # 拼接url地址，发送请求
        url = conf.get("env", "url") + case.url
        self.row = case.case_id + 1
        response = self.request.request(method=case.method, url=url, data=eval(case.request_data))  # 将str转换成dict

        if case.check_mysql:
            if "MemberId=#memberid5#" in case.check_mysql:
                case.check_mysql = data_replace(case.check_mysql)
                loanid = self.db.find_one(case.check_mysql)[0]
                setattr(ConText, "loanid", str(loanid))

        # 该打印的内容会显示在报告中
        print("请求数据--> {}".format(case.request_data))
        print("期望结果---> {}".format(case.expected_data))
        print("服务器响应数据--> {}".format(response.json()))

        res = {"status": response.json()["status"], "code": response.json()["code"]}

        try:
            # res = response.json()返回json格式，自动转换成Python的dict类型，只取部分字段进行断言
            # res = {"status": response.json()["status"], "code": response.json()["code"]}
            self.assertEqual(eval(case.expected_data), res)

            if case.check_mysql:
                if "竞标成功" in response.json()["msg"]:
                    # case.request_data是str类型，先转换为dict再来取值,float
                    money = eval(case.request_data)["amount"]
                    # 将float类型转换成decimal类型，与数据库查询的结果数据类型一致，并设置保留2位小数
                    money = Decimal.from_float(money).quantize(Decimal("0.00"))
                    after_money = self.db.find_one(case.check_mysql)[0]
                    # 该打印的内容会显示在报告中
                    print("投资前余额为:{}, 本次投资:{}, 投资后余额:{}".format(before_money, money, after_money))
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

    @classmethod
    def tearDownClass(cls):

        my_log.info("投资接口测试执行完毕......")
        cls.request.close()
        cls.db.close()
