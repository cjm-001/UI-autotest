#coding=utf-8
import os
from util.BrowserEngine import BrowserEngine
from Pages.TeacherListPage import TeacherListPage
from Pages.LoginPage import LoginPage
import unittest

class TeacherListCase(unittest.TestCase):
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
        print("打开讲师列表页case执行完成")

    def testOpenSubPages(self):
        """验证讲师列表页子页面可以正常访问"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.tg = TeacherListPage(self.driver)
        self.tg.click_teacherlist()
        self.tg.webdriverWait(10)
        self.tg.current_handle_switch()
        teachertext=self.tg.get_teachers_text()
        try:
            self.assertEqual(teachertext, "51CTO签约讲师")
            print("讲师列表页打开成功")
        except Exception as e:
            print("讲师列表页打开失败")
        # 验证讲师课程页面可以正常打开
        teacher_nick=self.tg.get_lec_nick()
        self.tg.click_lec_course_link()
        self.lg.webdriverWait(10)
        lec_nick_detail=self.tg.get_lec_nick_detail()
        try:
            self.assertEqual(lec_nick_detail,teacher_nick)
            print("讲师个人页打开成功")
        except Exception as e:
            print("讲师个人页打开失败")
        self.lg.back()
        # 验证讲师博客页面可以正常打开
        self.tg.click_lec_blog_link()
        self.lg.webdriverWait(10)
        self.lg.switch_window_without_close()
        try:
            assert u"-51CTO博客" in self.tg.get_page_title()
            print("讲师博客页面打开成功")
        except Exception as e:
            print("讲师博客页面打开失败",format(e))
        self.lg.webdriverWait(10)
        self.lg.switch_previous_window()
        #验证申请讲师页面可以正常打开
        self.tg.click_lec_apply()
        self.lg.webdriverWait(10)
        self.lg.switch_window_without_close()
        try:
            assert u"加入51CTO讲师团" in self.tg.get_page_title()
            print("申请讲师页面打开成功")
        except Exception as e:
            print("申请讲师页面打开失败",format(e))
        self.lg.webdriverWait(10)
        self.lg.switch_previous_window()
        #验证讲师大学页面可以正常打开
        self.tg.click_lec_college()
        self.tg.current_handle_switch()
        try:
            assert self.tg.get_enter_lec_button()
            print("讲师大学页面打开成功")
        except Exception as e:
            print("讲师大学页面打开失败",format(e))

if __name__ == '__main__':
    unittest.main()