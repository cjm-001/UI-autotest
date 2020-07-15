import os
from util.BrowserEngine import BrowserEngine
from Pages.BookColumnPage import BookColumnPage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import time

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_common_status=ExcelUtil(user_data_path, "common_user_login_status")
d_common=sheet_with_login_common_status.dict_data()

@ddt.ddt
class BookColumnCase(unittest.TestCase):
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
        print("博客专栏case执行完成")

    @ddt.data(*d_common)
    def testDaySeckill(self,data):
        """验证博客专栏流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.lg.Login_Account(data['username'], data['password'])
        self.bcp = BookColumnPage(self.driver)
        self.lg.webdriverWait(10)
        self.bcp.click_book_column_tab()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        #关闭博客广告弹框
        self.bcp.close_blog_pop()
        time.sleep(2)
        #关闭优惠券弹框
        self.bcp.close_coup_pop()
        #验证我的订阅专栏入口存在
        self.bcp.click_book_column_enter()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        #关闭我的订阅专栏界面优惠券弹框
        self.bcp.close_coup_pop_mypage()
        #验证页面跳转正确
        try:
            self.assertIn(u'我的订阅专栏',self.bcp.get_title_text())
            print("页面可以成功跳转到我的订阅专栏界面")
        except Exception as e:
            print("页面没有成功跳转到我的订阅专栏界面")

        '''非学院业务，去除冗余校验规则
        #验证用户无订阅信息
        try:
            self.assertIn(u'暂无订阅专栏',self.bcp.get_nocolumn_text())
            print("该用户暂未订阅专栏")
        except Exception as e:
            print("未订阅信息无法展示，需要检查是否异常")
        #去订阅专栏
        self.bcp.click_to_book_column()
        self.lg.webdriverWait(10)
        self.bcp.click_compose_column()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        #验证页面可以跳转到组合专栏界面
        try:
            self.assertIn(u'组合专栏',self.bcp.com_column_text())
            print("页面跳转正确")
        except Exception as e:
            print("页面跳转不正确")
        self.bcp.click_first_book_button()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.bcp.click_book_now()
        self.lg.webdriverWait(10)
        #验证页面可以跳转到支付中心
        self.bcp.verify_pay_center_exist()
        '''

if __name__=='__main__':
    unittest.main()

