#coding=utf-8
import os
from util.BrowserEngine import BrowserEngine
from Pages.CreateCouponPage import CreateCouponPage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import time

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_vip_status = ExcelUtil(user_data_path, "lecture")
d_lec = sheet_with_login_vip_status.dict_data()

@ddt.ddt
class CreateCouponCase(unittest.TestCase):
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
        print("讲师创建优惠券case执行完成")

    @ddt.data(*d_lec)
    def testTeacherCreateCourse(self,data):
        """验证讲师创建优惠券流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'], data['password'])
        self.ccp = CreateCouponPage(self.driver)
        #获取当前登录用户名
        self.ccp.enter_StudentCenter()
        log_user=self.ccp.get_username()
        print(log_user)

        #创建用于分配的优惠券
        time.sleep(2)
        self.lg.close_focus_pop()
        self.ccp.click_enterMarketingCenter()
        time.sleep(2)
        #self.lg.current_handle_switch()
        self.lg.close_teach_notice_pop()
        self.ccp.click_coup_tab()
        self.lg.webdriverWait(10)
        self.ccp.click_mark_center()
        self.lg.webdriverWait(10)
        self.ccp.click_create_coupon_button()
        time.sleep(2)
        coup_name_before=self.ccp.get_coup_name_before()
        self.ccp.enter_batch_price(5)
        self.ccp.enter_price_to(20)
        self.ccp.enter_gen_num(1)
        self.ccp.click_create_button()
        self.lg.webdriverWait(10)
        coup_name_after=self.ccp.get_coupon_name()
        try:
            assert coup_name_before==coup_name_after
            print("讲师优惠券名称获取成功")
        except Exception as e:
            print("讲师优惠券名称获取失败",format(e))
        #分配优惠券
        self.ccp.click_view_detail()
        self.lg.webdriverWait(10)
        try:
            assert u'未分配'==self.ccp.get_assign_status()
            print("优惠券分配前是状态正确")
        except Exception as e:
            print("优惠券分配前状态不正确")
        first_code=self.ccp.get_coupc_code_teacher()
        print(first_code)
        self.ccp.check_assign()
        self.ccp.click_assign_button()
        time.sleep(2)
        self.ccp.enter_assign_list(log_user)
        self.ccp.enter_assign_reason("测试优惠券分配")
        self.ccp.confirm_assign_oper()
        time.sleep(4)
        try:
            assert log_user==self.ccp.get_assign_user()
            print("优惠券已成功分配")
        except Exception as e:
            print("优惠券分配失败",format(e))
        time.sleep(2)
        #切换到学员中心查看分发的优惠券
        self.ccp.switch_person_center()
        time.sleep(2)
        self.lg.close_focus_pop()
        time.sleep(2)
        self.ccp.click_coup_user_tab()
        code_in_studentcenter=self.ccp.get_coup_code_student()
        print(code_in_studentcenter)
        try:
            self.assertIn(first_code,code_in_studentcenter)
            print("优惠券编码获取成功，分配成功")
        except Exception as e:
            print("优惠券分配失败")
        time.sleep(2)
        # 创建用于分配的优惠券
        self.ccp.click_enterMarketingCenter()
        #self.lg.current_handle_switch()
        time.sleep(2)
        self.ccp.click_coup_tab()
        self.lg.webdriverWait(10)
        self.ccp.click_mark_center()
        self.lg.webdriverWait(10)
        self.ccp.click_create_coupon_button()
        self.lg.webdriverWait(10)
        self.ccp.enter_batch_price(10)
        self.ccp.enter_price_to(35)
        self.ccp.enter_gen_num(1)
        self.ccp.click_create_button()
        self.lg.webdriverWait(10)
        self.ccp.click_view_detail()
        self.lg.webdriverWait(10)
        second_code=self.ccp.get_coupc_code_teacher()
        print(second_code)
        time.sleep(2)
        # 切换到学员中心验证优惠券激活功能正确
        self.ccp.switch_person_center()
        time.sleep(2)
        self.lg.close_focus_pop()
        self.ccp.click_coup_user_tab()
        time.sleep(2)
        self.ccp.type_activecode(second_code)
        self.ccp.click_active_button()
        time.sleep(4)
        second_code_in_studentcenter = self.ccp.get_coup_code_student()
        print(second_code_in_studentcenter)
        try:
            self.assertIn(second_code, second_code_in_studentcenter)
            print("优惠券编码获取成功，激活成功")
        except Exception as e:
            print("优惠券激活失败")
        time.sleep(2)

if __name__ == '__main__':
    unittest.main()

