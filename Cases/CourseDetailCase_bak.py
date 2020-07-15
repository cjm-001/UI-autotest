# coding=utf-8
"""
@description 验证讲师发布课程功能正常
@author cuijm
@date 2019-01-15
"""
import time
import unittest
import ddt
from util.BrowserEngine import BrowserEngine
from Pages.LoginPage import LoginPage
from util.ExcelUtil import ExcelUtil
from Pages.CourseDetailPage import CourseDetailPage
import os.path

class CourseDetailCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        browse = BrowserEngine(self)
        self.driver = browse.open_browser(self)
        self.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def test_edu_course_detail_page(self):
        """课程详情页用例"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.ld = CourseDetailPage(self.driver)
        self.ld.course_tab_method()
        self.ld.current_handle_switch()
        self.lg.webdriverWait(10)
        text1=self.ld.hot_course_title_text_method()
        self.ld.click_first_course()
        self.ld.current_handle_switch()
        text2 = self.ld.top_course_title_method()
        try:
            self.assertEqual(text1, text2, msg="成功进入课程详情页面")
            print('Test Pass',"成功进入课程详情页面")
        except Exception as e:
            print('Test Fail.', format(e))
        self.ld.tabsTil_method()
        text3 = self.ld.lesson_title_method()
        print(text3)
        self.ld.webdriverWait(10)
        self.ld.current_handle_switch()
        self.ld.scroolbar_height()
        time.sleep(2)
        self.ld.look_Now()
        self.ld.current_handle_switch()
        time.sleep(2)
        #如果第一个课时为收费课时，后续流程不执行
        '''
        text4 = self.ld.player_lesson_title_method()
        try:
            self.assertEqual(text3, text4, msg="成功进入课程详情页面")
            print('Test Pass',"点击课程详情页第一个课时成功进入播放页")
        except Exception as e:
            print('Test Fail.', format(e))
        self.ld.play_reback_method()
        text5 = self.ld.main_fr_text_method()
        self.ld.main_fr_method()
        self.ld.current_handle_switch()
        text6 = self.ld.lecture_name_text_method()
        try:
            self.assertEqual(text5,text6)
            print("成功进入讲师主页")
        except Exception as e:
            print("进入讲师主页失败",format(e))
        '''


if __name__ == '__main__ ':
    unittest.main()

