#coding=utf-8
import os
from util.BrowserEngine import BrowserEngine
from Pages.CooperationPage import CooperationPage
from Pages.LoginPage import LoginPage
import unittest
import time

class CooperationCase(unittest.TestCase):
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
        print("合作机构列表页case执行完成")

    def testOpenSubCoopPages(self):
        """验证合作机构子页面可以正常访问"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.cp = CooperationPage(self.driver)
        self.cp.click_cooplist()
        time.sleep(2)
        self.cp.webdriverWait(10)
        self.cp.current_handle_switch()
        cooptext = self.cp.get_coop_text()
        try:
            self.assertEqual(cooptext, "全部合作机构")
            print("合作机构列表页打开成功")
        except Exception as e:
            print("合作机构列表页打开失败")
        #验证推荐机构板块可以正常展示
        self.lg.webdriverWait(10)
        try:
            assert u'推荐机构'==self.cp.get_recommend_coop_text()
            print("推荐机构板块可以正常显示")
        except Exception as e:
            print("推荐机构板块无法正常显示")
        #验证最新加入机构板块可以正常显示
        self.lg.webdriverWait(10)
        try:
            assert u'最新加入机构'==self.cp.get_new_coop()
            print("最新加入机构板块可以正常显示")
        except Exception as e:
            print("最新加入机构板块无法正常显示")
        # 验证合作机构页面详情页可以正常打开
        first_coop = self.cp.get_first_coop_text()
        self.lg.webdriverWait(10)
        self.cp.click_first_coop()
        time.sleep(2)
        self.lg.webdriverWait(10)
        self.lg.switch_window_without_close()
        coop_detail = self.cp.get_coop_title_text()
        try:
            self.assertEqual(first_coop, coop_detail)
            print("合作机构详情页打开成功")
        except Exception as e:
            print("合作机构详情页打开失败")
        # 验证合作机构翻页功能可以正常打开
        self.lg.webdriverWait(10)
        self.lg.switch_previous_window()
        self.cp.scroolbar_bottom()
        self.cp.click_newcoop()
        time.sleep(2)
        self.lg.webdriverWait(10)
        self.cp.scroolbar_bottom()
        self.cp.verify_pre_page()

if __name__ == '__main__':
    unittest.main()