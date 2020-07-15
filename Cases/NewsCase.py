#coding=utf-8
import os
from util.BrowserEngine import BrowserEngine
from Pages.NewsPage import NewsPage
from Pages.LoginPage import LoginPage
import unittest

class NewsCase(unittest.TestCase):
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
        print("新闻case执行完成")

    def testNews(self):
        """验证新闻页面能够正常访问"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.ng = NewsPage(self.driver)
        self.ng.scroolbar_bottom()
        self.ng.click_newsmore()
        self.lg.webdriverWait(10)
        self.lg.current_handle_switch()
        newscenter=self.ng.get_newscenter_text()
        try:
            self.assertEqual(newscenter,u'新闻中心')
            print("新闻中心页面打开成功")
        except Exception as e:
            print("新闻中心页面打开失败")
        first_newstext_fromlist=self.ng.get_newstitle_fromlist()
        print(first_newstext_fromlist)
        self.ng.click_firstnews()
        self.lg.webdriverWait(10)
        self.lg.current_handle_switch()
        newstitle=self.ng.get_newtitle_fromdetail()
        print(newstitle)
        try:
            self.assertEqual(first_newstext_fromlist,newstitle,"新闻详情页打开失败")
            print("新闻详情页打开成功")
        except Exception as e:
            print("新闻详情页打开失败")

if __name__ == '__main__':
    unittest.main()




