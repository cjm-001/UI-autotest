#coding=utf-8
import os
from Pages.LoginPage import LoginPage
from util.BrowserEngine import BrowserEngine
from time import sleep
import unittest
from util.ExcelUtil import ExcelUtil
import ddt

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_login_success = ExcelUtil(user_data_path, "login_success")
d = sheet_login_success.dict_data()

sheet_with_login_error=ExcelUtil(user_data_path, "login_fail")
d_fail=sheet_with_login_error.dict_data()

@ddt.ddt
class LoginCase(unittest.TestCase):
    def setUp(self):
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)
        sleep(2)

    def tearDown(self):
        sleep(2)
        for method_name,error in self._outcome.errors:
            if error:
                case_name=self._testMethodName
                file_path=os.path.join(os.path.dirname(os.path.abspath('.'))+'/screenshot/'+case_name+'.png')
                self.driver.save_screenshot(file_path)
        self.driver.close()
        print("登录case执行完成")

    @ddt.data(*d)
    def testLoginSuccess(self,data):
        """验证会员用户和非会员用户可以登录成功"""
        print("当前测试数据是%s" % data)
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'],data['password'])

    @ddt.data(*d_fail)
    def atestLoginFail(self,data2):
        """验证登录失败场景"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(str(data2['username']),str(data2['password']))
        error_text=self.lg.get_error_info(str(data2['position']))
        try:
            self.assertEqual(data2['expected_message'],error_text)
            print("登录失败")
        except Exception as e:
            print("登录失败场景执行失败")


if __name__ == '__main__':
    unittest.main()



