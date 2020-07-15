import os
from util.BrowserEngine import BrowserEngine
from Pages.SignInPage import SignInPage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import time

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_vip_status = ExcelUtil(user_data_path, "vip_user_for_login_status")
d_vip = sheet_with_login_vip_status.dict_data()
sheet_with_login_common_status=ExcelUtil(user_data_path, "common_user_login_status")
d_common=sheet_with_login_common_status.dict_data()

@ddt.ddt
class SignInCase(unittest.TestCase):
    def setUp(self):
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)

    def tearDown(self):
        for method_name,error in self._outcome.errors:
            if error:
                case_name=self._testMethodName
                file_path=os.path.join(os.path.dirname(os.path.abspath('.'))+'/screenshot/'+case_name+'.png')
                self.driver.save_screenshot(file_path)
        self.driver.close()
        print("签到case执行完成")

    def testSignIn_notlogin(self):
        """验证未登录状态显示新人大礼包"""
        self.lg=LoginPage(self.driver)
        self.lg.close_active_pop()
        self.nl = SignInPage(self.driver)
        self.nl.click_newcomer()
        self.lg.current_handle_switch()
        time.sleep(2)
        self.nl.click_get_task()
        self.lg.webdriverWait(10)
        login_text = self.nl.get_login_text()
        print(login_text)
        try:
            self.assertEqual(login_text, u'注册')
            print('未登录状态下点击领取任务可以跳转到登录界面')
        except Exception as e:
            print('未登录状态下点击领取任务不能跳转到登录界面', format(e))

    @ddt.data(*d_vip)
    def testVipSignIn(self,data):
        """验证会员用户签到流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'], data['password'])
        self.siv = SignInPage(self.driver)
        self.lg.webdriverWait(10)
        #验证会员图标和翻倍图标可以展示
        self.siv.verify_vip_icon()
        self.siv.verify_vip_double()
        self.siv.verify_sign_button()

    @ddt.data(*d_common)
    def testnotVipSignIn(self, data):
        """验证非会员用户签到流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'], data['password'])
        self.sin = SignInPage(self.driver)
        self.lg.webdriverWait(10)
        self.sin.verify_sign_button()

if __name__ == '__main__':
    unittest.main()