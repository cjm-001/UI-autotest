import os
from util.BrowserEngine import BrowserEngine
from Pages.LimitFreePage import LimitFreePage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import time

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_vip_status = ExcelUtil(user_data_path, "vip_user_for_login_status")
d_vip = sheet_with_login_vip_status.dict_data()

@ddt.ddt
class LimitFreeCase(unittest.TestCase):
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
        print("新课限免case执行完成")

    @ddt.data(*d_vip)
    def testVipFreeCourse(self, data):
        """验证会员限免流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.lg.Login_Account(data['username'], data['password'])
        self.lfp = LimitFreePage(self.driver)
        self.lg.webdriverWait(10)
        self.lfp.click_limit_free()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        #验证新课限免板块定位正确
        try:
            self.assertIn(u'新课限免',self.lfp.get_new_course_free())
            print("页面可以成功跳转到新课限免板块")
        except Exception as e:
            print("新课限免板块定位不到")
        #验证第一个课程为VIP免费课程
        try:
            self.assertEqual(u'免费',self.lfp.first_free_label())
            print("第一个课程为vip免费课程")
        except Exception as e:
            print("第一个课程无法获取到vip免费标识")
        #验证会员可以免费观看限免课程
        self.lfp.click_first_pic()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.lfp.verify_limit_free_button()
        time.sleep(2)
        self.lfp.click_course_list()
        self.lfp.verify_chap_icon()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        #验证课时播放页存在会员限免按钮
        self.lfp.get_vip_free_button()

if __name__ == '__main__':
        unittest.main()

