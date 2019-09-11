# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/14

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
from common.tools import rand_phone, data_replace
from common.execute_mysql import ExecuteMysql


# 从配置文件获取数据
file_name = conf.get('excel', 'file_name')
read_column = conf.get('excel', 'read_column')
read_column = eval(read_column)     # 将str转换成list


@ddt
class RegisterTestCase(unittest.TestCase):

    # 拼接完整的excel路径，然后读取excel数据
    wb = ReadExcel(os.path.join(DATA_DIR, file_name), "register")
    cases = wb.read_column_data(read_column)

    @classmethod
    def setUpClass(cls):
        my_log.info("============================== 准备开始执行注册接口的测试 ==============================")
        cls.request = HTTPRequest2()
        cls.db = ExecuteMysql()

    @classmethod
    def tearDownClass(cls):
        my_log.info("============================== 注册接口测试执行完毕 ==============================")
        cls.request.close()

    @data(*cases)   # 拆包，拆成几个参数
    def test_register(self, case):
        # 筛选用例的请求数据中做了#register__phone#标记的数据
        if "#register_phone#" in case.request_data:
            while True:
                # 生成随机号码
                mobile_phone = rand_phone("133")
                # 查询数据库有无该随机号码
                count = self.db.find_count("SELECT Id FROM member WHERE MobilePhone={}".format(mobile_phone))
                # 数据库中无此随机号码，就不用继续随机生成，直接使用该随机号码
                if count == 0:
                    break
            # 将用例中的#register__phone#替换成随机生成的手机号码
            case.request_data = case.request_data.replace("#register_phone#", mobile_phone)

        # 从数据库中查询一个已注册号码给用例
        elif "#exists_phone#" in case.request_data:
            # 从数据库获取第一条号码，给用例参数
            mobile_phone = self.db.find_one("SELECT MobilePhone FROM member LIMIT 1")[0]
            # 用从数据库获取的号码替换掉请求数据中的标记#exists_phone
            case.request_data = case.request_data.replace("#exists_phone#", mobile_phone)

        # 替换各号段的手机号码
        case.request_data = data_replace(case.request_data)

        # 拼接url地址
        url = conf.get("env", "url") + case.url
        # 行数等于用例编号+1
        self.row = case.case_id + 1
        response = self.request.request(method=case.method, url=url, data=eval(case.request_data))

        # 该打印的内容会显示在报告中
        print("请求数据--> {}".format(case.request_data))
        print("期望结果--> {}".format(case.expected_data))
        print("服务器响应数据--> {}".format(response.json()))

        res = response.json()

        try:
            self.assertEqual(eval(case.expected_data), res)
        except AssertionError as e:
            result = 'FAIL'
            my_log.exception(e)     # 将异常信息记录到日志
            raise e
        else:
            result = 'PASS'
            my_log.info("预期结果:{}, 实际结果:{}, 断言结果:{}".format(eval(case.expected_data), res, result))
        finally:
            # 向Excel回写服务器返回结果
            self.wb.write_data(row=self.row, column=9, value=str(res))
            # 向Excel回写断言结果
            self.wb.write_data(row=self.row, column=10, value=result)
