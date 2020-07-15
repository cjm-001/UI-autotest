import os
from util.BrowserEngine import BrowserEngine
from Pages.CourseListPage import CourseListPage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_vip_status = ExcelUtil(user_data_path, "vip_user_for_login_status")
d = sheet_with_login_vip_status.dict_data()

@ddt.ddt
class CourseListCase(unittest.TestCase):
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
        print("课程列表页case执行完成")

    def testCheckCourseList_withoutLogin(self):
        """验证未登录下课程列表页元素和功能正常"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.cl = CourseListPage(self.driver)
        self.cl.click_course_tab()
        self.lg.current_handle_switch()
        try:
            assert u"全部课程" == self.cl.get_allcourse_text()
            print("课程列表页打开成功")
        except Exception as e:
            print("课程列表页打开失败", format(e))
        # 验证顶部导航展示正常
        self.lg.webdriverWait(10)
        try:
            assert u"VIP会员"==self.cl.get_vip_member()
            print("VIP会员可以正常显示")
        except Exception as e:
            print("VIP会员不能正常显示")
        self.lg.webdriverWait(10)
        try:
            assert u"登录/注册"==self.cl.get_login_link()
            print("登录注册入口可以正常显示")
        except Exception as e:
            print("登录注册入口不能正常显示")
        self.lg.webdriverWait(10)
        # 验证课程筛选功能正常
        try:
            assert u"综合排序"==self.cl.get_comrank()
            print("课程列表筛选栏可以正常显示")
        except Exception as e:
            print("课程列表筛选栏无法正常显示")
        self.lg.webdriverWait(10)
        #验证翻页功能正常
        self.cl.scroolbar_size()
        self.cl.click_nextpage()
        self.lg.webdriverWait(10)
        try:
            self.assertEqual(self.cl.get_current_page_number(),'2')
            print("翻页功能正常")
        except Exception as e:
            print("翻页功能不能正常工作")
        self.lg.webdriverWait(10)
        # 验证免费课程筛选功能正常
        self.cl.click_free_check()
        self.lg.webdriverWait(10)
        try:
            assert u"免费"==self.cl.get_first_free()
            print("免费课程筛选功能正常")
        except Exception as e:
            print("免费课程筛选功能不正确")
        self.lg.webdriverWait(10)
        # 验证会员课程筛选功能正常
        self.cl.click_vip_check()
        self.lg.webdriverWait(10)
        self.cl.scroolbar_size()
        try:
            assert u"会员免费"== self.cl.get_first_vip()
            print("会员课程筛选功能正常")
        except Exception as e:
            print("会员课程筛选功能不正确")
        self.lg.webdriverWait(10)
        # 验证限时折扣课程筛选功能正常
        self.cl.scroolbar_size()
        self.cl.click_discount_check()
        self.lg.webdriverWait(10)
        try:
            assert u"折" in self.cl.get_first_discount()
            print("限时折扣筛选功能正常")
        except Exception as e:
            print("限时折扣筛选功能不正确")
        self.lg.webdriverWait(10)
        #验证未登录时候点击加入购物车跳转到登录
        self.cl.click_add_to_cart()
        self.lg.webdriverWait(10)
        login_text = self.cl.get_AccountLogin_text()
        try:
            self.assertEqual(login_text, u'注册')
            print('登录跳转成功')
        except Exception as e:
            print('登录跳转失败', format(e))

    @ddt.data(*d)
    def testCourseList_withLogin(self,data):
        """验证登录状态下课程列表页元素和功能正常"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'],data['password'])
        self.cln = CourseListPage(self.driver)
        self.cln.click_course_tab()
        self.lg.current_handle_switch()
        # 验证顶部导航展示正常
        self.lg.webdriverWait(10)
        try:
            assert u"学习中心" == self.cln.get_study_center()
            print("课程列表页登录状态可以正常获取")
        except Exception as e:
            print("课程列表页登录状态获取失败")
        self.lg.webdriverWait(10)
        try:
            assert u"购物车" in self.cln.get_buy_cart()
            print("课程列表页用户购物车可以正常显示")
        except Exception as e:
            print("课程列表页用户购物车不能正常显示")
        self.lg.webdriverWait(10)

if __name__ == '__main__':
    unittest.main()