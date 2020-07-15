import os
from util.BrowserEngine import BrowserEngine
from Pages.TopicListPage import TopicListPage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_vip_status = ExcelUtil(user_data_path, "vip_user_for_login_status")
d = sheet_with_login_vip_status.dict_data()

@ddt.ddt
class TopicListCase(unittest.TestCase):
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
        print("专题列表页case执行完成")

    def testTopicList(self):
        """验证未登录下专题列表页元素和功能正常"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.tl = TopicListPage(self.driver)
        self.tl.click_topic_tab()
        self.lg.current_handle_switch()
        try:
            assert u"全部" == self.tl.get_all_toic()
            print("专题列表页打开成功")
        except Exception as e:
            print("专题列表页打开失败", format(e))
        self.lg.webdriverWait(10)
        # 验证顶部导航展示正常
        self.lg.webdriverWait(10)
        try:
            assert u"VIP会员" == self.tl.get_vip_icon()
            print("VIP会员可以正常显示")
        except Exception as e:
            print("VIP会员不能正常显示")
        self.lg.webdriverWait(10)
        try:
            assert u"登录/注册" == self.tl.get_reg_login()
            print("登录注册入口可以正常显示")
        except Exception as e:
            print("登录注册入口不能正常显示")
        self.lg.webdriverWait(10)
        # 验证专题列表有专题数据
        self.tl.scroolbar_bottom()
        try:
            assert u"条记录" in self.tl.get_record_sum()
            print("专题列表页有专题数据记录")
        except Exception as e:
            print("专题列表页每页专题数据记录")
        self.lg.webdriverWait(10)
        # 验证翻页功能正常
        self.tl.click_next_page()
        self.tl.scroolbar_bottom()
        try:
            assert u"首页" == self.tl.get_first_page()
            print("专题列表页翻页功能正常")
        except Exception as e:
            print("专题列表页翻页功能异常")
        #验证进入专题详情页功能正常
        self.tl.scroolbar_top()
        self.tl.click_first_topic()
        self.lg.switch_window_without_close()
        try:
            assert u"专题价" in self.tl.get_topic_price()
            print("专题详情页可以正常打开")
        except Exception as e:
            print("专题详情页无法打开")

    @ddt.data(*d)
    def testTopicList_withLogin(self,data):
        """验证登录状态下专题列表页元素和功能正常"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'],data['password'])
        self.tln = TopicListPage(self.driver)
        self.tln.click_topic_tab()
        self.lg.current_handle_switch()
        # 验证顶部导航展示正常
        self.lg.webdriverWait(10)
        try:
            assert u"学习中心" == self.tln.get_study_center()
            print("专题列表页登录状态可以正常获取")
        except Exception as e:
            print("专题列表页登录状态获取失败")
        self.lg.webdriverWait(10)
        try:
            assert u"购物车" in self.tln.get_buy_cart()
            print("专题列表页用户购物车可以正常显示")
        except Exception as e:
            print("专题列表页用户购物车不能正常显示")

if __name__ == '__main__':
    unittest.main()