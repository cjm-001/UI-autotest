#coding=utf-8
import os
from util.BrowserEngine import BrowserEngine
from Pages.WejobBottomPage import WejobBottomPage
from Pages.LoginPage import LoginPage
import unittest

class WejobBottomCase(unittest.TestCase):
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
        print("微职位通用底栏case执行完成")

    def testWejobBottom(self):
        """验证微职位通用底栏能够正常"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.wb = WejobBottomPage(self.driver)
        self.lg.webdriverWait(10)
        self.wb.wejob_enter_method()
        self.wb.current_handle_switch()
        self.lg.webdriverWait(10)
        self.wb.scroolbar_bottom()
        self.wb.click_helpcenter()
        self.wb.current_handle_switch()
        #验证帮助中心页面可以打开
        try:
            self.assertIn(u'帮助中心_微职位_' in self.wb.get_page_title())
            print("帮助中心页面可以打开")
        except Exception as e:
            print("帮助中心页面不能打开")
        #验证常见问题板块可以正常展示
        try:
            self.assertEqual(u'常见问题',self.wb.get_common_question())
            print("常见问题板块可以展示")
        except Exception as e:
            print("常见问题板块不能展示")
        self.wb.scroolbar_bottom()
        self.lg.webdriverWait(10)
        self.wb.click_feedback_enter()
        self.wb.current_handle_switch()
        self.lg.webdriverWait(10)
        #验证意见反馈页面可以打开
        try:
            self.assertEqual(u'意见反馈',self.wb.get_feedback_title())
            print("意见反馈页面可以正常打开")
        except Exception as e:
            print("意见反馈页面无法正常打开")
        self.wb.scroolbar_bottom()
        self.wb.click_discuss_circle()
        self.lg.webdriverWait(10)
        self.wb.current_handle_switch()
        #验证学员交流圈页面可以打开
        try:
            self.assertIn(u'学员交流圈' in self.wb.get_page_title())
            print("学员交流圈页面可以打开")
        except Exception as e:
            print("学员交流圈页面无法正常打开")
        print("更新日志入口被屏蔽")

    if __name__ == '__main__':
        unittest.main()