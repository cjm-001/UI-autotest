import os
from util.BrowserEngine import BrowserEngine
from Pages.CourseBuyPage import CourseBuyPage
from Pages.LoginPage import LoginPage

import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import re
import time

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_vip_status = ExcelUtil(user_data_path, "vip_user_for_login_status")
d_vip = sheet_with_login_vip_status.dict_data()
sheet_with_login_common_status=ExcelUtil(user_data_path, "common_user_login_status")
d_common=sheet_with_login_common_status.dict_data()

@ddt.ddt
class CourseBuyCase(unittest.TestCase):
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
        print("课程购买case执行完成")

    @ddt.data(*d_common)
    def testCommonUser_VipCourseBuy(self, data2):
        """验证非会员用户购买会员课程流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data2['username'], data2['password'])
        self.vc = CourseBuyPage(self.driver)
        self.vc.click_course_tab()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.vc.click_vip_check()
        self.lg.webdriverWait(10)
        self.vc.scroolbar_size()
        self.vc.click_first_course()
        self.lg.webdriverWait(10)
        self.lg.current_handle_switch()
        # 获取课程详情页会员课程价格并下单
        vip_course_price=self.vc.get_vip_course_price()
        print(vip_course_price)
        time.sleep(2)
        self.vc.close_weixin_pop()
        self.vc.click_buynow()
        time.sleep(2)
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        time.sleep(2)
        vip_price=self.vc.get_vip_price_confirmpage()
        print(vip_price)
        try:
            self.assertIn(vip_price, vip_course_price)
            print("会员课程在订单确认页价格显示正确")
        except Exception as e:
            print("会员课程在订单确认页价格显示不正确")
        sum_vip_price = self.vc.get_sum_price()
        print(sum_vip_price)
        try:
            self.assertEqual(vip_price, sum_vip_price)
            print("会员课程价格计算正确")
        except Exception as e:
            print("会员课程价格计算不正确")
        # 验证会员课程订单确认页价格正确
        self.vc.click_vip_balance()
        self.vc.handle_topay_pop()
        time.sleep(2)
        self.lg.webdriverWait(10)
        vip_course_price_confirmpage = self.vc.get_confirm_price_paypage()
        print(vip_course_price_confirmpage)
        try:
            self.assertEqual(vip_course_price_confirmpage, sum_vip_price)
            print("会员课程在订单确认页价格正确")
        except Exception as e:
            print("会员课程在订单确认页价格不正确")
        self.lg.webdriverWait(10)
        # 验证订单可以成功提交
        self.vc.verify_to_pay_page()
        time.sleep(3)
        # 验证待支付订单可以创建
        self.vc.click_my_pay_center()
        self.lg.webdriverWait(10)
        self.lg.current_handle_switch()
        vip_price_in_paycenter = self.vc.get_order_price_paycenter()
        try:
            self.assertEqual(vip_price_in_paycenter, sum_vip_price)
            print("待支付订单可以成功创建")
        except Exception as e:
            print("待支付订单不能成功创建")
        # 验证待支付订单可以被删除、实现数据初始化
        self.vc.click_first_delete()
        self.driver.switch_to_alert().accept()
        print("会员课程订单删除了")

    @ddt.data(*d_vip)
    def testVipUser_NonDiscountCourseBuy(self,data3):
        """验证会员用户购买原价课程可以享受95折"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data3['username'], data3['password'])
        self.ncb = CourseBuyPage(self.driver)
        self.ncb.input_teacher("王顶")
        self.ncb.click_search_home()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.ncb.verify_list_course_click()
        self.lg.webdriverWait(10)
        self.lg.current_handle_switch()
        time.sleep(2)
        self.ncb.close_weixin_pop()
        non_discount_detail_price=self.ncb.get_non_discount_price()
        print("课程详情页价格为："+non_discount_detail_price)
        self.ncb.click_buynow()
        time.sleep(2)
        self.lg.webdriverWait(10)
        self.lg.current_handle_switch()
        #验证会员用户可以享受会员95折扣
        try:
            self.assertEqual(u'会员9.5折',self.ncb.get_vip_ninefive())
            print("会员用户购买原价课程可以享受会员95折")
        except Exception as e:
            print("会员用户购买原价课程不可以享受会员95折")
        time.sleep(2)
        settlement_price = self.ncb.get_sum_price()
        print("订单确认页支付价格："+settlement_price)
        #判断是否有待支付订单，删除
        self.ncb.click_vip_balance()
        self.ncb.handle_topay_pop()
        self.lg.webdriverWait(10)
        # 验证会员用户购买原价课程在支付页面价格正确
        time.sleep(2)
        last_price_topay = self.ncb.get_price_topay()
        try:
            self.assertEqual(settlement_price,last_price_topay)
            print("会员用户购买原价课程在支付页面价格正确")
        except Exception as e:
            print("会员用户购买原价课程在支付页面价格不正确")
        self.lg.webdriverWait(10)
        # 验证订单可以成功提交
        self.ncb.verify_to_pay_page()
        # 验证待支付订单可以创建
        self.ncb.click_my_pay_center()
        self.lg.webdriverWait(10)
        self.lg.current_handle_switch()
        vip_price_in_paycenter = self.ncb.get_order_price_paycenter()
        try:
            self.assertEqual(vip_price_in_paycenter, settlement_price)
            print("待支付订单可以成功创建")
        except Exception as e:
            print("待支付订单不能成功创建")
        # 验证待支付订单可以被删除、实现数据初始化
        self.ncb.click_first_delete()
        self.driver.switch_to_alert().accept()
        print("会员用户购买原价课程订单删除了")

    @ddt.data(*d_common)
    def testCommonUser_NonDiscountCourseBuy(self,data4):
        """验证非会员用户购买原价课程需要原价支付"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data4['username'], data4['password'])
        self.ccb = CourseBuyPage(self.driver)
        self.ccb.input_teacher("王顶")
        self.ccb.click_search_home()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.ccb.verify_list_course_click()
        self.lg.webdriverWait(10)
        self.lg.current_handle_switch()
        time.sleep(2)
        self.ccb.close_weixin_pop()
        non_discount_detail_price=self.ccb.get_non_discount_price()
        print("课程详情页价格："+non_discount_detail_price)
        self.ccb.click_buynow()
        time.sleep(2)
        self.lg.webdriverWait(10)
        self.lg.current_handle_switch()
        #验证非会员用户需要原价购买
        time.sleep(2)
        dis_confirm_price=self.ccb.get_vip_price_confirmpage()
        print("订单确认页价格："+dis_confirm_price)
        try:
            self.assertIn(dis_confirm_price,non_discount_detail_price)
            print("订单确认页价格正确")
        except Exception as e:
            print("订单确认页价格不正确")
        # 判断是否有待支付订单，删除
        self.ccb.click_vip_balance()
        self.ccb.handle_topay_pop()
        time.sleep(2)
        self.lg.webdriverWait(10)
        # 验证非会员用户购买原价课程在支付页面价格正确
        last_price_topay = self.ccb.get_price_topay()
        try:
            self.assertEqual(dis_confirm_price,last_price_topay)
            print("非会员用户购买原价课程在支付页面价格正确")
        except Exception as e:
            print("非会员用户购买原价课程在支付页面价格不正确")
        self.lg.webdriverWait(10)
        # 验证订单可以成功提交
        self.ccb.verify_to_pay_page()
        # 验证待支付订单可以创建
        self.ccb.click_my_pay_center()
        self.lg.webdriverWait(10)
        self.lg.current_handle_switch()
        try:
            self.assertEqual(dis_confirm_price, last_price_topay)
            print("待支付订单可以成功创建")
        except Exception as e:
            print("待支付订单不能成功创建")
        # 验证待支付订单可以被删除、实现数据初始化
        self.ccb.click_first_delete()
        self.driver.switch_to_alert().accept()
        print("会员用户购买原价课程订单删除了")

if __name__ == '__main__':
    unittest.main()
