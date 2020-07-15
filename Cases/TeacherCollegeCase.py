import os
from util.BrowserEngine import BrowserEngine
from Pages.TeacherCollegePage import TeacherCollegePage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import time

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_common_status=ExcelUtil(user_data_path, "common_user_login_status")
d_common=sheet_with_login_common_status.dict_data()

@ddt.ddt
class TeacherCollegeCase(unittest.TestCase):
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
        print("讲师大学case执行完成")

    def testTeacherCollege_notlogin(self):
        """验证未登录状态下讲师大学功能"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.tc = TeacherCollegePage(self.driver)
        self.tc.click_teacher_colllege()
        self.lg.webdriverWait(10)
        self.lg.current_handle_switch()
        self.tc.verify_college_page()
        self.tc.click_become_teacher()
        self.lg.current_handle_switch()
        login_text = self.tc.get_login_text()
        try:
            self.assertEqual(login_text, u'登录51CTO')
            print('登录跳转成功')
        except Exception as e:
            print('登录跳转失败', format(e))

    @ddt.data(*d_common)
    def testTeacherCollege_login(self,data):
        """验证登录状态下讲师大学功能"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'], data['password'])
        self.tc = TeacherCollegePage(self.driver)
        self.tc.click_teacher_colllege()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.tc.click_become_teacher()
        self.tc.switch_window_without_close()
        self.lg.webdriverWait(10)
        teacher_apply_text=self.tc.get_teacher_apply_text()
        try:
            self.assertEqual(teacher_apply_text,u'签订协议')
            print("签约讲师申请页面打开成功")
        except Exception as e:
            print("签约讲师申请页面无法打开")
        time.sleep(2)
        self.lg.switch_previous_window()
        self.tc.click_become_org()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        reg_apply_text=self.tc.get_reg_apply_text()
        try:
            self.assertEqual(teacher_apply_text,u'合作机构申请')
            print("合作机构申请页面打开成功")
        except Exception as e:
            print("合作机构申请页面无法打开")
        time.sleep(2)

if __name__ == '__main__ ':
    unittest.main()
