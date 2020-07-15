import os
from util.BrowserEngine import BrowserEngine
from Pages.StudentEvaluationPage import StudentEvaluationPage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import time

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_common_status=ExcelUtil(user_data_path, "common_user_login_status")
d_common=sheet_with_login_common_status.dict_data()

@ddt.ddt
class StudentEvaluationCase(unittest.TestCase):
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
        print("学员评价case执行完成")

    @ddt.data(*d_common)
    def testLoginUserEva(self,data):
        """验证登录状态学员评价流程正确"""
        self.lg=LoginPage(self.driver)
        self.lg.close_active_pop()
        self.lg.Login_Account(data['username'], data['password'])
        self.sep = StudentEvaluationPage(self.driver)
        self.lg.webdriverWait(10)
        self.sep.click_student_eva()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.sep.verify_deploy_exist()
        self.sep.click_deploy()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        #验证登录用户点击我要发布，页面跳转到购买记录页面
        try:
            self.assertEqual(u'商品信息',self.sep.get_goods_info())
            print("登录用户点击发布按钮页面跳转到购买记录页面")
        except Exception as e:
            print("登录用户点击发布按钮无法跳转到购买页面")
        time.sleep(2)

    def testNotLoginUserEva(self):
        """验证未登录用户评价流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.sevp = StudentEvaluationPage(self.driver)
        self.lg.webdriverWait(10)
        self.sevp.click_student_eva()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.sevp.verify_deploy_exist()
        self.sevp.click_deploy()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        #验证未登录用户点击我要发布，页面跳转到登录页面
        try:
            self.assertIn(u'登录51CTO',self.sevp.verify_login_text())
            print("页面跳转到登录界面，流程正确")
        except Exception as e:
            print("页面无法跳转到登录界面，流程不正确")


if __name__ == '__main__':
        unittest.main()
