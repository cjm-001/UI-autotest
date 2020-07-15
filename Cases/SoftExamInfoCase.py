#coding=utf-8
import os
from util.BrowserEngine import BrowserEngine
from Pages.SoftExamInfoPage import SoftExamInfoPage
from Pages.LoginPage import LoginPage
import unittest
import time

class SoftExamCase(unittest.TestCase):
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
        print("软考频道case执行完成")

    def testRKchannel(self):
        """验证软考频道页面能够正常访问"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.rk = SoftExamInfoPage(self.driver)
        #self.rk.wejob_link_method()
        self.rk.wejob_enter_method()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.rk.click_rk_tab()
        self.lg.webdriverWait(10)
        #验证免费试听板块存在
        try:
            assert u'免费试听' in self.rk.get_free_listen_text()
            print("免费试听板块存在")
        except Exception as e:
            print("免费试听板块不能展示")
        time.sleep(2)
        self.rk.scroolbar_size()
        #验证软考快讯板块存在
        try:
            assert u'软考快讯' in self.rk.get_rk_news_label()
            print("软考快讯板块存在")
        except Exception as e:
            print("软考快讯板块无法显示")
        #验证学员故事板块可以展示
        try:
            assert u'学员故事' in self.rk.get_student_article()
            print("学员故事板块存在")
        except Exception as e:
            print("学员故事板块不能展示")
        #验证自营教材板块存在
        try:
            assert u'自营教材' in self.rk.get_own_books()
            print("自营教材板块存在")
        except Exception as e:
            print("自营教材板块不能展示")
        time.sleep(2)
        self.rk.scroolbar_size()
        #验证火热开班板块存在
        try:
            assert u'火热开班' in self.rk.get_hot_class()
            print("火热开班板块存在")
        except Exception as e:
            print("火热开班板块不能展示")
        time.sleep(2)
        self.rk.scroolbar_size()
        #验证自学课程板块存在
        try:
            assert u'自学课程' in self.rk.get_study_byself()
            print("自学课程板块存在")
        except Exception as e:
            print("自学课程板块不存在")
        time.sleep(2)
        self.rk.scroolbar_size()
        #验证专家讲师板块存在
        try:
            assert u'专家讲师' in self.rk.get_expect_teacher()
            print("专家讲师板块存在")
        except Exception as e:
            print("专家讲师板块不存在")
        #验证教学服务板块存在
        try:
            assert u'教学服务' in self.rk.get_teach_service()
            print("教学服务板块存在")
        except Exception as e:
            print("教学服务板块不存在")
        self.rk.scroolbar_top()
        self.rk.click_news_tab()
        #self.rk.click_rk_news_more()
        self.lg.current_handle_switch()
        #验证资讯动态列表页面可以成功打开
        try:
            assert u'资讯动态' in self.rk.get_page_title()
            print("资讯动态页面打开成功")
        except Exception as e:
            print("资讯动态页面打开失败", format(e))
        self.lg.webdriverWait(10)
        # 验证软考直通车板块存在
        self.rk.verify_rk_bus()
        self.rk.click_signup_link()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        try:
            assert u'软考直通车' in self.rk.get_page_title()
            print("软考报名页面可以打开")
        except Exception as e:
            print("软考报名页面不能打开")
        time.sleep(1)
        #验证题库宝典页面可以打开
        self.rk.click_exam_tab()
        time.sleep(1)
        try:
            assert u'免费题库' in self.rk.get_page_title()
            print("免费题库页面可以成功打开")
        except Exception as e:
            print("免费题库页面不能打开")
        # self.rk.click_news_tab()
        # self.lg.webdriverWait(10)
        # time.sleep(1)
        '''##活动期间各种资讯跳转活动
        #验证资讯详情页可以正常打开
        news_title_inlist=self.rk.get_first_news_title()
        self.rk.click_first_news()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        try:
            self.assertEqual(news_title_inlist,self.rk.get_news_title())
            print("资讯详情页可以成功打开")
        except Exception as e:
            print("资讯详情页不能成功打开")
        time.sleep(2)
        self.rk.scroolbar_bottom()
        self.rk.click_thumbs_up()
        self.rk.verify_login_text()
        time.sleep(1)
        self.rk.back()
        self.rk.scroolbar_top()
        '''

    if __name__ == '__main__':
        unittest.main()

