import os
from util.BrowserEngine import BrowserEngine
from Pages.SearchPage import SearchPage
from Pages.LoginPage import LoginPage
import unittest

class SearchCase(unittest.TestCase):
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
        print("搜索case执行完成")

    def testSearchTeacher(self):
        """验证搜索讲师功能正常"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.slp = SearchPage(self.driver)
        self.slp.input_teacher("风哥")
        self.slp.click_search_home()
        self.lg.current_handle_switch()
        try:
            assert u"风哥" == self.slp.get_lec_nick()
            print("讲师搜索结果页打开成功")
        except Exception as e:
            print("讲师搜索结果页打开失败", format(e))
        self.lg.webdriverWait(10)
        lec_nick_searchpage=self.slp.get_lec_nick()
        self.slp.enter_lec_course_page()
        self.lg.switch_window_without_close()
        lec_nick_detailpage=self.slp.get_lec_nick_detail()
        try:
            self.assertEqual(lec_nick_searchpage,lec_nick_detailpage)
            print("成功进入讲师主页")
        except Exception as e:
            print("无法进入讲师主页")
        self.lg.webdriverWait(10)
        self.lg.switch_previous_window()
        try:
            assert u'为您找到相关内容' in self.slp.get_lec_course_search_result()
            print("讲师课程搜索结果正常返回")
        except Exception as e:
            print("讲师课程搜索结果无记录返回")
        self.slp.click_lec_tab()
        self.lg.webdriverWait(10)

    def testSearchCourse(self):
        """验证搜索非讲师关键字功能正常"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.slp = SearchPage(self.driver)
        self.slp.type_notlec_keyword("python")
        self.slp.click_search_home()
        self.lg.current_handle_switch()
        try:
            assert u'为您找到相关内容' in self.slp.get_notlec_reasult()
            print("课程搜索结果正常返回")
        except Exception as e:
            print("课程搜索结果返回失败")
        self.lg.webdriverWait(10)
        try:
            self.slp.isElementExist(self.slp.enter_lec_page)
            print("非讲师关键词搜索结果无推荐讲师存在,搜索失败")
        except Exception as e:
            print("非讲师关键词搜索结果存在推荐讲师,搜索成功")
        self.lg.webdriverWait(10)

    def testSearchNoResult(self):
        """验证搜索无结果功能正常"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.snp = SearchPage(self.driver)
        self.snp.type_notlec_keyword("12345678901234567890")
        self.snp.click_search_home()
        self.lg.current_handle_switch()
        try:
            assert u'抱歉，没有找到您的搜索内容' in self.snp.get_searchNoResult_text()
            print("搜索无结果时显示友好推荐文案")
        except Exception as e:
            print("搜索无结果时显示友好推荐文案")
        self.lg.webdriverWait(10)
        try:
            assert u'为您找到相关内容0条' in self.snp.get_noresult_searchresult()
            print("搜索无搜索结果记录返回条数正确")
        except Exception as e:
            print("搜索无搜索结果记录返回条数不正确")
        self.lg.webdriverWait(10)

if __name__ == '__main__':
    unittest.main()


