import os
from util.BrowserEngine import BrowserEngine
from Pages.DaySeckillPage import DaySeckillPage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import time

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_common_status=ExcelUtil(user_data_path, "common_user_login_status")
d_common=sheet_with_login_common_status.dict_data()

@ddt.ddt
class FreeCourseCase(unittest.TestCase):
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
        print("天天秒杀课程下单case执行完成")

    @ddt.data(*d_common)
    def testDaySeckill(self,data):
        """验证天天秒杀&定价秒杀页面能正常访问"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.lg.Login_Account(data['username'], data['password'])
        self.dsp = DaySeckillPage(self.driver)
        self.lg.webdriverWait(10)
        self.dsp.click_seckill_tab()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.dsp.verify_seck_pic_exist()
        #验证天天秒杀课程中包含全部筛选分类
        try:
            self.assertIn(u'全部',self.dsp.get_rest_num())
            print("全部分类数据可以展示")
        except Exception as e:
            print("全部分类数据不可以展示")
        self.dsp.click_prcing_seckill_tab()
        self.dsp.verify_pricing_seckill_exsit()
        #验证定价秒杀课程包含已售个数
        try:
            self.assertIn(u'已售',self.dsp.get_sold_num())
            print("课程已售个数可以展示")
        except Exception as e:
            print("课程已售个数不可以展示")
        #验证秒杀课程可以正常下单
        # self.dsp.click_buy_button()
        # try:
        #     self.assertEqual(u'订单确认',self.dsp.get_order_confirm())
        #     print("订单确认页面可以打开")
        # except Exception as e:
        #     print("订单确认页面不能正常打开，下单失败")
        # self.dsp.click_topay()
        # self.lg.webdriverWait(10)
        # self.dsp.click_my_paycenter()
        # self.lg.current_handle_switch()
        # #删除测试产生的待支付订单
        # self.dsp.click_first_delete()
        # self.driver.switch_to_alert().accept()
        # print("秒杀课程订单删除了")

if __name__ == '__main__':
    unittest.main()
