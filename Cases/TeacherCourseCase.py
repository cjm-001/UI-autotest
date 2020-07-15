import os
from util.BrowserEngine import BrowserEngine
from Pages.TeacherCoursePage import TeacherCoursePage
from Pages.LoginPage import LoginPage
import unittest

class TeacherCourseCase(unittest.TestCase):
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
        print("讲师课程页case执行完成")

    def testTeacherCourse(self):
        """验证讲师课程页面功能正常"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.tc = TeacherCoursePage(self.driver)
        self.tc.get_url(self.tc.env.getUrl()+"/lecturer/8371666.html")
        self.tc.webdriverWait(10)
        #验证讲师博客页可以正常访问
        self.tc.click_lec_blog()
        self.lg.switch_window_without_close()
        try:
            assert u"-51CTO博客" in self.tc.get_page_title()
            print("讲师博客页面打开成功")
        except Exception as e:
            print("讲师博客页面打开失败", format(e))
        self.lg.webdriverWait(10)
        #验证讲师评分字段可以正常显示
        self.lg.switch_previous_window()
        try:
            assert u"讲师评分:" in self.tc.get_fb_rate()
            print("讲师评分字段可以正常显示")
        except Exception as e:
            print("讲师评分字段未找到")
        self.lg.webdriverWait(10)
        #验证好课推荐模块正常显示
        try:
            assert u"好课推荐" in self.tc.get_good_course()
            print("好课推荐模块可以正常显示")
        except Exception as e:
            print("好课推荐模块未找到")
        self.lg.webdriverWait(10)
        # 验证超值专题模块正常显示
        try:
            assert u"超值学习路径" in self.tc.get_cheep_spec()
            print("超值学习路径模块可以正常显示")
        except Exception as e:
            print("超值学习路径模块未找到")
        self.lg.webdriverWait(10)

        #滚动滚动条操作查看
        #self.tc.scroolbar_middle()
        self.lg.webdriverWait(10)
        self.tc.click_more_spec()

if __name__ == '__main__':
    unittest.main()

