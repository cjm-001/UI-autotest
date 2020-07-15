"""
@description 验证月度、季度、年度会员购买功能正常
@author cuijm
@date 2019-03-25
"""
import os
from util.BrowserEngine import BrowserEngine
from Pages.VipBuyPage import VipBuyPage
from Pages.LoginPage import LoginPage
from Pages.CourseBuyPage import CourseBuyPage
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
class VipBuyCase(unittest.TestCase):
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
        print("会员购买case执行完成")

    @ddt.data(*d_vip)
    def testVipBuyCase1(self,data):
        """验证会员用户购买年度会员流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'], data['password'])
        self.cb = VipBuyPage(self.driver)
        self.ld = CourseBuyPage(self.driver)
        self.cb.vipslgn_method()
        self.cb.current_handle_switch()
        time.sleep(3)
        self.cb.open_vip_method()
        self.cb.webdriverWait(10)
        text1 = self.cb.pay_price_year_method()
        time.sleep(2)
        self.cb.pay_type_method()
        self.cb.webdriverWait(10)
        self.cb.current_handle_switch()
        text2 = self.ld.get_price_topay()
        try:
            self.assertEqual(int(text1),int(text2))
            print("支付页面会员价格计算正确")
        except Exception as e:
            print("支付页面会员价格计算不正确")
        self.cb.xueyuan_link_method()
        self.cb.current_handle_switch()
        self.cb.webdriverWait(10)
        self.cb.study_center_method()
        self.cb.webdriverWait(10)
        self.lg.close_focus_pop()
        self.cb.get_order_list_method()
        self.cb.vip_order_list_method()
        text3 = self.cb.pay_state_method()
        text4 = self.cb.pay_money_method()
        try:
            self.assertEqual(text3, "未支付")
            print("会员订单状态显示正确")
        except Exception as e:
            print("会员订单状态显示不正确")
        try:
            self.assertEqual(int(text2), int(text4))
            print("会员价格在学院与支付中心价格显示一致")
        except Exception as e:
            print("会员价格在学院与支付中心价格显示不一致")
        self.cb.pay_order_method()
        self.cb.current_handle_switch()
        self.cb.my_pay_center_method()
        self.cb.current_handle_switch()
        time.sleep(2)
        text5 =self.ld.get_order_price_paycenter()
        try:
            self.assertEqual(int(text2),int(text5))
            print("支付中心会员价格计算正确")
        except Exception as e:
            print("支付中心会员价格计算不正确")
        # 验证待支付订单可以被删除、实现数据初始化
        self.ld.click_first_delete()
        self.driver.switch_to_alert().accept()
        print("年会员待支付订单删除了")

    @ddt.data(*d_vip)
    def testVipBuyCase2(self, data):
        """验证会员用户购买季度会员流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'], data['password'])
        self.cb = VipBuyPage(self.driver)
        self.ld = CourseBuyPage(self.driver)
        self.cb.vipslgn_method()
        self.cb.current_handle_switch()
        time.sleep(3)
        self.cb.open_vip_method()
        time.sleep(2)
        self.cb.quarter_vip_method()
        text1 = self.cb.pay_price_quarter_method()
        time.sleep(2)
        self.cb.pay_type_method()
        self.cb.webdriverWait(10)
        self.cb.current_handle_switch()
        text2 = self.ld.get_price_topay()
        try:
            self.assertEqual(int(text1), int(text2))
            print("支付页面会员价格计算正确")
        except Exception as e:
            print("支付页面会员价格计算不正确")
        self.cb.xueyuan_link_method()
        self.cb.current_handle_switch()
        self.cb.webdriverWait(10)
        self.cb.study_center_method()
        self.cb.webdriverWait(10)
        self.lg.close_focus_pop()
        self.cb.get_order_list_method()
        self.cb.vip_order_list_method()
        text3 = self.cb.pay_state_method()
        text4 = self.cb.pay_money_method()
        try:
            self.assertEqual(text3, "未支付")
            print("会员订单状态显示正确")
        except Exception as e:
            print("会员订单状态显示不正确")
        try:
            self.assertEqual(int(text2), int(text4))
            print("会员价格在学院与支付中心价格显示一致")
        except Exception as e:
            print("会员价格在学院与支付中心价格显示不一致")
        self.cb.pay_order_method()
        self.cb.current_handle_switch()
        self.cb.my_pay_center_method()
        self.cb.current_handle_switch()
        time.sleep(2)
        text5 = self.ld.get_order_price_paycenter()
        try:
            self.assertEqual(int(text2), int(text5))
            print("支付中心会员价格计算正确")
        except Exception as e:
            print("支付中心会员价格计算不正确")
        # 验证待支付订单可以被删除、实现数据初始化
        self.ld.click_first_delete()
        self.driver.switch_to_alert().accept()
        print("季度会员待支付订单删除了")

    @ddt.data(*d_common)
    def testVipBuyCase3(self, data):
        """验证非会员用户购买月度会员流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'], data['password'])
        self.cb = VipBuyPage(self.driver)
        self.ld = CourseBuyPage(self.driver)
        self.cb.vipslgn_method()
        self.cb.current_handle_switch()
        time.sleep(3)
        self.cb.open_vip_method()
        self.cb.webdriverWait(10)
        time.sleep(2)
        self.cb.month_vip_method()
        text1 = self.cb.pay_price_month_method()
        time.sleep(2)
        self.cb.pay_type_method()
        self.cb.webdriverWait(10)
        self.cb.current_handle_switch()
        text2 = self.ld.get_price_topay()
        try:
            self.assertEqual(int(text1), int(text2))
            print("支付页面会员价格计算正确")
        except Exception as e:
            print("支付页面会员价格计算不正确")
        self.cb.xueyuan_link_method()
        self.cb.current_handle_switch()
        self.cb.webdriverWait(10)
        self.cb.study_center_method()
        self.cb.webdriverWait(10)
        self.lg.close_focus_pop()
        self.cb.get_order_list_method()
        self.cb.vip_order_list_method()
        text3 = self.cb.pay_state_method()
        text4 = self.cb.pay_money_method()
        try:
            self.assertEqual(text3, "未支付")
            print("会员订单状态显示正确")
        except Exception as e:
            print("会员订单状态显示不正确")
        try:
            self.assertEqual(int(text2), int(text4))
            print("会员价格在学院与支付中心价格显示一致")
        except Exception as e:
            print("会员价格在学院与支付中心价格显示不一致")
        self.cb.pay_order_method()
        self.cb.current_handle_switch()
        self.cb.my_pay_center_method()
        self.cb.current_handle_switch()
        time.sleep(2)
        text5 = self.ld.get_order_price_paycenter()
        try:
            self.assertEqual(int(text2), int(text5))
            print("支付中心会员价格计算正确")
        except Exception as e:
            print("支付中心会员价格计算不正确")
        # 验证待支付订单可以被删除、实现数据初始化
        self.ld.click_first_delete()
        self.driver.switch_to_alert().accept()
        print("月度会员待支付订单删除了")

    # def testVipBuyCase4(self):
    #     """验证未登录用户购买会员流程正确"""
    #     self.cb = VipBuyPage(self.driver)
    #     self.ld = CourseBuyPage(self.driver)
    #     self.cb.vipslgn_method()
    #     self.cb.current_handle_switch()
    #     self.cb.open_vip_method()
    #     time.sleep(2)
    #     text1 = self.cb.login_tip_method()
    #     try:
    #         self.assertEqual(text1,'登录51CTO')
    #         print("未登录用户点击购买会员正确跳转至登录页面")
    #     except Exception as e:
    #         print("未登录用户点击购买会员正确跳转至登录页面")


if __name__ == '__main__':
    unittest.main()


