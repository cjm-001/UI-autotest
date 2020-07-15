#coding=utf-8
import os
from Pages.FavoritesPage import FavoritesPage
from util.BrowserEngine import BrowserEngine
from Pages.LoginPage import LoginPage
from time import sleep
import unittest
from util.ExcelUtil import ExcelUtil
import ddt

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_vip_status = ExcelUtil(user_data_path, "vip_user_for_login_status")
d = sheet_with_login_vip_status.dict_data()

@ddt.ddt
class FavoritesCase(unittest.TestCase):
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
        print("收藏case执行完成")

    def testCourseFav_notlogin(self):
        """验证未登录状态下收藏功能"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.fg = FavoritesPage(self.driver)
        self.fg.get_url(self.fg.env.getUrl()+"/course/571.html")
        self.fg.click_fav_course_icon()
        self.fg.webdriverWait(10)
        login_text=self.fg.get_AccountLogin_text()
        try:
            self.assertEqual(login_text,u'注册')
            print('登录跳转成功')
        except Exception as e:
            print('登录跳转失败', format(e))

    @ddt.data(*d)
    def testCourseFav_login(self,data):
        """验证登录状态下收藏功能"""
        print("当前测试数据是%s" % data)
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'], data['password'])
        self.fp = FavoritesPage(self.driver)
        self.fp.get_url(self.fp.env.getUrl()+"/course/571.html")
        self.lg.webdriverWait(10)
        course_fav_num_org=self.fp.get_fav_course_number()
        print(course_fav_num_org)
        sleep(2)
        self.fp.close_weixin_pop()
        course_title_org=self.fp.get_coursetitle_text()
        self.fp.click_fav_course_icon()
        sleep(2)
        course_fav_num_update = self.fp.get_fav_course_number()
        print(course_fav_num_update)
        try:
            self.assertNotEqual(course_fav_num_org,course_fav_num_update)
            print('收藏数量变化成功，收藏成功')
        except Exception as e:
            print('收藏人数没有变化，收藏失败', format(e))
        sleep(3)
        #检验学习中心收藏功能
        self.fp.click_StudyCenter()
        sleep(3)
        self.lg.close_focus_pop()
        sleep(2)
        self.fp.click_myfav()
        sleep(3)
        course_title_sec=self.fp.get_favcoursetitle_text()
        try:
            self.assertEqual(course_title_org, course_title_sec)
            print('收藏课程标题获取成功，收藏成功')
        except Exception as e:
            print('收藏课程标题获取不成功，收藏失败', format(e))
        #取消收藏
        self.fp.get_url(self.fp.env.getUrl()+"/course/571.html")
        self.fp.webdriverWait(2)
        self.fp.click_fav_course_icon()
        sleep(3)

if __name__ == '__main__ ':
    unittest.main()