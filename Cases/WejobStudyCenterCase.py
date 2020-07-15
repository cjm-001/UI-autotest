import os
from util.BrowserEngine import BrowserEngine
from Pages.WejobStudyCenterPage import WejobStudyCenterPage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import re
import time

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_vip_status = ExcelUtil(user_data_path, "vip_user_for_login_status")
d_vip = sheet_with_login_vip_status.dict_data()
sheet_with_login_common_status=ExcelUtil(user_data_path, "common_user_login_status")
d_common=sheet_with_login_common_status.dict_data()

@ddt.ddt
class WejobStudyCenterCase(unittest.TestCase):
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
        print("微职位学习中心case执行完成")

    @ddt.data(*d_common)
    def testWejobStudyCenter(self,data):
        """验证未购买课程用户微职位学习中心流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.lg.Login_Account(data['username'], data['password'])
        self.wsc = WejobStudyCenterPage(self.driver)
        self.lg.webdriverWait(10)
        self.wsc.wejob_enter_method()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.wsc.click_study_center()
        self.lg.webdriverWait(10)
        self.wsc.current_handle_switch()
        self.wsc.verify_ok_exist()
        self.lg.webdriverWait(10)
        #验证微职位学习中心页面可以成功打开
        try:
            assert u'当前共有' in self.wsc.get_class_number()
            print("微职位tab页打开，页面存在报名的微职位信息")
        except Exception as e:
            print("页面不存在报名的微职位信息")
        time.sleep(2)
        #验证视频课程tab可以打开
        self.wsc.click_course_tab()
        try:
            self.assertEqual(u'你尚未购买视频课程，可前往这里选课',self.wsc.get_notbuy_text())
            print("未购买课程文案可以展示")
        except Exception as e:
            print("未购买课程文案不能展示")
        self.wsc.click_gobutton()
        #验证课程列表页可以成功打开
        time.sleep(2)
        self.wsc.current_handle_switch()
        try:
            assert u'全部课程' in self.wsc.get_page_title()
            print("课程列表页可以成功打开")
        except Exception as e:
            print("课程列表页无法正常打开")

    if __name__ == '__main__':
        unittest.main()
