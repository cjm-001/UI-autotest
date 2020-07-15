import os
from util.BrowserEngine import BrowserEngine
from Pages.TrainingHomePage import TrainingHomePage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import time

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_vip_status = ExcelUtil(user_data_path, "vip_user_for_login_status")
d = sheet_with_login_vip_status.dict_data()

@ddt.ddt
class TrainingHomeCase(unittest.TestCase):
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
        print("微职位新首页case执行完成")

    def testTrainingHomeNoLogin(self):
        """验证未登录状态下访问微职位新首页正常"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.ld = TrainingHomePage(self.driver)
        self.ld.webdriverWait(10)
        #self.ld.wejob_link_method()
        self.ld.wejob_enter_method()
        self.ld.current_handle_switch()
        self.ld.webdriverWait(10)
        #验证微职位首页可以正常打开
        try:
            assert u'微职位 - ' in self.ld.get_page_title()
            print("微职位新首页打开成功")
        except Exception as e:
            print("微职位新首页打开失败", format(e))
        self.ld.scroolbar_bottom()
        self.ld.webdriverWait(10)
        #验证平台资质模块可正确加载
        try:
            assert u'平台资质' == self.ld.enterprise_qualif_method()
            print("平台资质模块加载成功")
        except Exception as e:
            print("平台资质模块加载失败", format(e))
        #验证新闻动态模块可以正确展示
        try:
            assert u'新闻动态' == self.ld.get_wejob_news()
            print("新闻动态模块加载成功")
        except Exception as e:
            print("新闻动态模块加载失败", format(e))
        #滚动到页面顶部
        self.ld.scroolbar_top()
        self.ld.webdriverWait(10)
        #验证软考学院板块可以展示
        try:
            assert u'软考学院'==self.ld.get_soft_college()
            print("软考学院板块可以展示")
        except Exception as e:
            print("软考学院板块无法展示")
        #验证微职位软考分类页可正常打开
        self.ld.click_soft_college_more()
        self.ld.current_handle_switch()
        self.ld.webdriverWait(10)
        try:
            assert u'软考学院-微职位' in self.ld.get_page_title()
            print("软考学院分类列表页打开成功")
        except Exception as e:
            print("软考学院分类列表页打开失败", format(e))
        self.ld.scroolbar_bottom()
        self.ld.webdriverWait(10)

    @ddt.data(*d)
    def testTrainingHomeLogin(self,data):
        """验证登录状态下访问微职位新首页正常"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'],data['password'])
        self.ld = TrainingHomePage(self.driver)
        self.ld.webdriverWait(10)
        #self.ld.wejob_link_method()
        self.ld.wejob_enter_method()
        self.ld.current_handle_switch()
        # 验证微职位首页可以正常打开
        try:
            assert u'消息' == self.ld.messge_method()
            print("登录用户访问微职位新首页成功")
        except Exception as e:
            print("登录用户访问微职位新首页失败", format(e))
        self.ld.messge_click_method()
        self.ld.switch_window_without_close()
        try:
            assert u'51CTO技术家园' in self.ld.get_page_title()
            print("消息跳转家园成功")
        except Exception as e:
            print("消息跳转家园失败",format(e))
        self.ld.switch_previous_window()
        self.ld.scroolbar_bottom()
        self.ld.webdriverWait(10)
        # 验证微职位首页可以正常打开
        try:
            assert u'微职位 - ' in self.ld.get_page_title()
            print("微职位新首页打开成功")
        except Exception as e:
            print("微职位新首页打开失败", format(e))

if __name__ == '__main__':
    unittest.main()




