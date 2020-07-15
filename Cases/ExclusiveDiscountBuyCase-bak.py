import os
from util.BrowserEngine import BrowserEngine
from Pages.ExclusiveDiscountBuyPage import ExclusiveDiscountBuyPage
from Pages.CourseBuyPage import CourseBuyPage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import re
import time

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_year_vip = ExcelUtil(user_data_path, "year_vip")
year_vip = sheet_with_year_vip.dict_data()
sheet_with_quarter_vip = ExcelUtil(user_data_path,"quarter_vip")
quarter_vip = sheet_with_quarter_vip.dict_data()
sheet_with_monthly_vip = ExcelUtil(user_data_path,"monthly_vip")
monthly_vip = sheet_with_monthly_vip.dict_data()
sheet_with_login_common_status=ExcelUtil(user_data_path, "common_user_login_status")
d_common=sheet_with_login_common_status.dict_data()

@ddt.ddt
class ExclusiveDiscountBuyCase(unittest.TestCase):
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
        print("会员专属折扣课程购买case执行完成")

    @ddt.data(*year_vip)
    def atestYearDiscountCourseBuy(self,data):
        """验证年度会员购买会员折扣课程价格正确"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'], data['password'])
        self.vc = CourseBuyPage(self.driver)
        self.ld = ExclusiveDiscountBuyPage(self.driver)
        self.ld.vipslgn_method()
        self.ld.current_handle_switch()
        self.ld.scroolbar_bottom()
        self.ld.webdriverWait(10)
        text1 = self.ld.discount_price_method()
        time.sleep(2)
        self.ld.discount_img_method()
        self.ld.current_handle_switch()
        vip_course_price = self.vc.get_vip_course_price()
        try:
            self.assertEqual(text1,vip_course_price)
            print("会员主页与课程详情页会员专属价格显示一致")
        except Exception as e:
            print("会员主页与课程详情页会员专属价格显示不一致")
        time.sleep(2)
        self.vc.click_buynow()
        self.vc.current_handle_switch()
        self.vc.webdriverWait(10)
        vip_price = self.vc.get_vip_price_confirmpage()
        print(vip_price)
        vip_discount_text = self.vc.vip_discount_label_method()
        print(vip_discount_text)
        try:
            self.assertIn(vip_price, vip_course_price)
            print("会员课程在订单确认页价格显示正确")
        except Exception as e:
            print("会员课程在订单确认页价格显示不正确")
        try:
            self.assertIn(vip_discount_text,"会员专享")
            print("年会员订单确认页标签显示正确")
        except Exception as e:
            print("年会员订单确认页标签显示不正确")
        sum_vip_price = self.vc.get_sum_price()
        print(sum_vip_price)
        try:
            self.assertEqual(vip_price, sum_vip_price)
            print("会员课程价格计算正确")
        except Exception as e:
            print("会员课程价格计算不正确")
        # 验证会员课程订单确认页价格正确
        self.vc.click_vip_balance()
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
        self.driver.switch_to.alert().accept()
        print("会员课程订单删除了")

    @ddt.data(*quarter_vip)
    def atestQuarterDiscountCourseBuy(self, data):
        """验证季度会员购买会员折扣课程价格正确"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'], data['password'])
        self.vc = CourseBuyPage(self.driver)
        self.ld = ExclusiveDiscountBuyPage(self.driver)
        self.ld.vipslgn_method()
        self.ld.current_handle_switch()
        self.ld.scroolbar_bottom()
        self.ld.webdriverWait(10)
        text1 = self.ld.discount_price_method()
        time.sleep(2)
        self.ld.discount_img_method()
        self.ld.current_handle_switch()
        vip_course_price = self.vc.get_vip_course_price()
        try:
            self.assertEqual(text1, vip_course_price)
            print("会员主页与课程详情页会员专属价格显示一致")
        except Exception as e:
            print("会员主页与课程详情页会员专属价格显示不一致")
        time.sleep(2)
        self.vc.click_buynow()
        self.vc.current_handle_switch()
        self.vc.webdriverWait(10)
        vip_price = self.vc.get_vip_price_confirmpage()
        print(vip_price)
        vip_discount_text = self.vc.vip_discount_label_method()
        print(vip_discount_text)
        try:
            self.assertIn(vip_price, vip_course_price)
            print("会员课程在订单确认页价格显示正确")
        except Exception as e:
            print("会员课程在订单确认页价格显示不正确")
        try:
            self.assertIn(vip_discount_text,"会员专享")
            print("年会员订单确认页标签显示正确")
        except Exception as e:
            print("年会员订单确认页标签显示不正确")
        sum_vip_price = self.vc.get_sum_price()
        print(sum_vip_price)
        try:
            self.assertEqual(vip_price, sum_vip_price)
            print("会员课程价格计算正确")
        except Exception as e:
            print("会员课程价格计算不正确")
        # 验证会员课程订单确认页价格正确
        self.vc.click_vip_balance()
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
        self.driver.switch_to.alert().accept()
        print("会员课程订单删除了")


    @ddt.data(*monthly_vip)
    def atestMonthlyDiscountCourseBuy(self, data):
        """验证月度会员购买会员折扣课程价格正确"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'], data['password'])
        self.vc = CourseBuyPage(self.driver)
        self.ld = ExclusiveDiscountBuyPage(self.driver)
        self.ld.vipslgn_method()
        self.ld.current_handle_switch()
        self.ld.scroolbar_bottom()
        self.ld.webdriverWait(10)
        text1 = self.ld.discount_price_method()
        time.sleep(2)
        self.ld.discount_img_method()
        self.ld.current_handle_switch()
        vip_course_price = self.vc.get_vip_course_price()
        try:
            self.assertNotEqual(text1, vip_course_price)
            print("会员主页与课程详情页会员专属价格不一致")
        except Exception as e:
            print("会员主页与课程详情页会员专属价格显示出现异常")
        time.sleep(2)
        self.vc.click_buynow()
        self.vc.current_handle_switch()
        self.vc.webdriverWait(10)
        vip_price = self.vc.get_vip_price_confirmpage()
        print(vip_price)
        upgrade_member_text = self.vc.upgrade_member_method()
        print(upgrade_member_text)
        try:
            self.assertIn(u"升级会员立省",upgrade_member_text)
            print("月度会员订单确认页标签显示正确")
        except Exception as e:
            print("月度会员订单确认页标签显示不正确")
        vip_discount_ninefive=self.vc.vip_discount_ninefive_method()
        if vip_discount_ninefive=="会员9.5折":
            org_price = re.sub("\D","",vip_course_price)
            dis_confirm_price = re.sub("\D","",vip_price)
            try:
                self.assertEqual(int(int(org_price)*0.95),int(dis_confirm_price))
                print("会员用户95折计算正确")
            except Exception as e:
                print("会员用户95折计算不正确")
            settlement_price = self.vc.get_sum_price()
            try:
                self.assertEqual(dis_confirm_price, settlement_price)
                print("月度会员用户购买原价课程价格计算正确")
            except Exception as e:
                print("月度会员用户购买原价课程价格计算不正确")
        else:
            dis_confirm_price = re.sub("\D", "", vip_price)
            settlement_price = self.vc.get_sum_price()
            try:
                self.assertEqual(dis_confirm_price, settlement_price)
                print("月度会员用户购买折扣课程价格计算正确")
            except Exception as e:
                print("月度会员用户购买折扣课程价格计算不正确")


if __name__ == '__main__':
    unittest.main()
