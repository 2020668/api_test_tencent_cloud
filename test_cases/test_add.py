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
from common.tools import data_replace

# 从配置文件获取数据
file_name = conf.get('excel', 'file_name')
read_column = conf.get('excel', 'read_column')
read_column = eval(read_column)     # 将str转换成list


@ddt
class AddTestCase(unittest.TestCase):

    # 拼接完整的excel路径，然后读取excel数据
    wb = ReadExcel(os.path.join(DATA_DIR, file_name), "add")
    cases = wb.read_column_data(read_column)

    @classmethod
    def setUpClass(cls):
        my_log.info("======== 准备开始执行加标接口的测试 ========")
        cls.request = HTTPRequest2()
        cls.db = ExecuteMysql()

    @classmethod
    def tearDownClass(cls):
        my_log.info("======== 加标接口测试执行完毕 ========")
        cls.request.close()
        cls.db.close()

    @data(*cases)   # 拆包，拆成几个参数
    def test_add(self, case):
        case.request_data = data_replace(case.request_data)

        if case.check_mysql:
            case.check_mysql = data_replace(case.check_mysql)
            before_count = self.db.find_count(case.check_mysql)

        # 拼接url地址，发送请求
        url = conf.get("env", "url") + case.url
        self.row = case.case_id + 1
        response = self.request.request(method=case.method, url=url, data=eval(case.request_data))  # 将str转换成dict
        # 该打印的内容会显示在报告中
        print("请求数据--> {}".format(case.request_data))
        print("期望结果--> {}".format(case.expected_data))
        print("服务器响应数据--> {}".format(response.json()))

        # res = response.json()返回json格式，自动转换成Python的dict类型，只取部分字段进行断言
        res = {"status": response.json()["status"], "code": response.json()["code"]}

        try:
            self.assertEqual(eval(case.expected_data), res)

            if case.check_mysql:
                case.check_mysql = data_replace(case.check_mysql)
                after_count = self.db.find_count(case.check_mysql)
                member_id = eval(case.request_data)["memberId"]
                message = self.db.find_one("SELECT * FROM loan WHERE memberid={} ORDER BY CreateTime DESC LIMIT 1".format(member_id))
                print("最近一条标的信息为：{}".format(message))
                print("加标之前该用户的标数量为：{},加标后标数量为：{}".format(before_count, after_count))
                self.assertEqual(before_count + 1, after_count)

        except AssertionError as e:
            result = 'FAIL'
            my_log.exception(e)     # 将异常信息记录到日志
            raise e
        else:
            result = 'PASS'
            my_log.info("预期结果：%s, 实际结果：%s, 测试通过" % (eval(case.expected_data), res))

        finally:
            self.wb.write_data(row=self.row, column=10, value=str(res))
            self.wb.write_data(row=self.row, column=11, value=result)
