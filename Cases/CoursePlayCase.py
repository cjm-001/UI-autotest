import os
from util.BrowserEngine import BrowserEngine
from Pages.CoursePlayPage import CoursePlayPage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import re
import time

@ddt.ddt
class CoursePlayCase(unittest.TestCase):
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
        print("视频播放页case执行完成")

    def testNologin