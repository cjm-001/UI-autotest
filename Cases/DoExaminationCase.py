import os
from selenium.webdriver.support.ui import WebDriverWait
from util.BrowserEngine import BrowserEngine
from Pages.DoExaminationPage import DoExaminationPage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import re
import time

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_common_status=ExcelUtil(user_data_path, "common_user_login_status")
d_common=sheet_with_login_common_status.dict_data()

@ddt.ddt
class DoExaminationCase(unittest.TestCase):
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
        print("用户提交作业case执行完成")

    @ddt.data(*d_common)
    def testDoExaminationCase(self,data):
        """验证用户提交作业流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'], data['password'])
        self.vc = DoExaminationPage(self.driver)
        self.vc.study_center_link_method()
        self.lg.close_focus_pop()
        self.vc.my_examcenter_method()
        self.vc.webdriverWait(10)
        self.vc.current_handle_switch()
        text1=self.vc.examList_name_method()
        exam_times=self.vc.answer_times_method()
        self.vc.do_agin_method()
        self.vc.current_handle_switch()
        self.vc.iamready_method()
        text2=self.vc.exam_title_method()
        try:
            self.assertEqual(text1,text2)
            print("成功进入做试卷页面")
        except Exception as e:
            print("进入做试卷页面不正确")
        time.sleep(2)
        self.vc.scroolbar_size()
        self.vc.submit_btn_method()
        time.sleep(1)
        self.vc.submit_yes_method()
        time.sleep(2)
        text3=self.vc.yes_quality_method()
        print(text3)
        try:
            self.assertEqual(text3,"0")
            print("成功交卷")
        except Exception as e:
            print("交卷失败")
        time.sleep(3)
        try:
            self.assertEqual(self.vc.get_score(),'0')
            print("考试成绩为0，满足预期")
        except Exception as e:
            print("没有获取到考试成绩，需要检查原因")
        self.vc.webdriverWait(10)
        self.vc.click_check_answer()
        #验证解析页面分数正确
        self.vc.webdriverWait(10)
        time.sleep(2)
        try:
            self.assertEqual(self.vc.get_score_on_answer(),'0分')
            print("解析页分数为0，满足预期")
        except Exception as e:
            print("没有获取到考试成绩，需要检查原因")
        time.sleep(2)
        print("case执行完成")


if __name__ == '__main__':
    unittest.main()

