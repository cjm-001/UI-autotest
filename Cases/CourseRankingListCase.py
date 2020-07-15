#coding=utf-8
import os
from util.BrowserEngine import BrowserEngine
from Pages.CourseRankingListPage import CourseRankingListPage
from Pages.LoginPage import LoginPage
import unittest
import time

class CourseRankingListCase(unittest.TestCase):
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
        print("课程排行榜case执行完成")

    def testCourseRankingList(self):
        """验证课程排行榜页面能够正常访问"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.cr = CourseRankingListPage(self.driver)
        self.cr.click_ranklist()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.cr.verify_rank_pic()
        #验证第一名课程可以展示
        self.cr.verify_first_num()
        self.cr.scroolbar_bottom()
        self.cr.click_next_page()
        self.cr.click_first_fav()
        self.lg.webdriverWait(10)
        self.cr.verify_login_text()
        self.cr.back()
        #验证学习人数榜可以打开
        self.cr.click_study_nums()
        try:
            assert u'学习人数榜' in self.cr.get_page_title()
            print("学习人数榜页面可以成功打开")
        except Exception as e:
            print("学习人数榜页面不能打开")
        self.lg.webdriverWait(10)
        # 验证课程受欢迎榜可以打开
        self.cr.click_popular_list()
        try:
            assert u'课程受欢迎榜' in self.cr.get_page_title()
            print("课程受欢迎榜页面可以成功打开")
        except Exception as e:
            print("课程受欢迎榜页面不能打开")
        self.lg.webdriverWait(10)
        # 验证新课热卖榜可以打开
        self.cr.click_new_course()
        try:
            assert u'新课热卖榜' in self.cr.get_page_title()
            print("新课热卖榜页面可以成功打开")
        except Exception as e:
            print("新课热卖榜页面不能打开")
        self.lg.webdriverWait(10)
        # 验证好评榜可以打开
        self.cr.click_praise_list()
        try:
            assert u'课程好评榜' in self.cr.get_page_title()
            print("课程好评榜页面可以成功打开")
        except Exception as e:
            print("课程好评榜页面不能打开")
        self.lg.webdriverWait(10)
        #验证免费试看页面可以打开
        first_title=self.cr.get_first_course_title()
        self.cr.click_free_look()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        try:
            self.assertEqual(first_title, self.cr.get_course_title_detail())
            print("第一名课程详情页可以成功打开")
        except Exception as e:
            print("第一名课程详情页不能成功打开")
        time.sleep(2)

    if __name__ == '__main__':
        unittest.main()

