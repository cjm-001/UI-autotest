#coding=utf-8
import os
from util.BrowserEngine import BrowserEngine
from Pages.StudyCenterPage import StudyCenterPage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import time

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_vip_status = ExcelUtil(user_data_path, "vip_user_for_login_status")
d_vip = sheet_with_login_vip_status.dict_data()

@ddt.ddt
class StudyCenterCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        browse = BrowserEngine(self)
        self.driver = browse.open_browser(self)
        self.driver.implicitly_wait(10)
    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    @ddt.data(*d_vip)
    def test_edu_studycenter_01(self,data):
        """已登录进入学员中心"""
        lg = LoginPage(self.driver)
        lg.Login_Account(data['username'], data['password'])
        homepage = StudyCenterPage(self.driver)
        nickname_before = homepage.shouye_nickname_text()
        homepage.study_center_click()
        time.sleep(1)
        lg.close_focus_pop()
        time.sleep(2)
        abc_after = homepage.nichen_get()
        try:
            self.assertEqual(nickname_before,abc_after,msg="成功进入学习中心页面")
            print('Test Pass')
        except Exception as e:
            print('Test Fail.', format(e))
        homepage.xufei_vip_method()
        lg.switch_window()
        try:
            assert '51CTO VIP会员' in homepage.get_page_title()
            print('Test Pass.')
        except Exception as e:
            print('Test Fail.',format(e))
        lg.switch_One_window()
        homepage.pay_gold_method()
        lg.switch_window()
        try:
            assert '余额充值' in homepage.get_page_title()
            print('Test Pass.')
        except Exception as e:
            print('Test Fail.',format(e))
        homepage.switch_One_window()
        time.sleep(2)

    def test_edu_studycenter_02(self):
        """学习的课程"""
        ld = StudyCenterPage(self.driver)
        ld.get_url(ld.env.getUrl() + "/center/course/user/get-study-course")
        text1 = ld.wejob_text_method()
        text2 = ld.course_text_method()
        before = ld.wejob_title_text_method()
        try:
            self.assertEqual(text1,u'微职位',msg="我的微职位加载成功")
            self.assertEqual(text2,u'课程',msg="我的课程加载成功")
            print('Test Pass.',"成功加载微职位、课程")
        except Exception as e:
            print('Test Fail.',format(e))
        ld.wejob_title_method()
        ld.switch_window()
        after = ld.Myclass_wejob_title_method()
        try:
            self.assertEqual(before,after,msg="微职位标题一致")
            print('Test Pass.',"微职位标题检查一致")
        except Exception as e:
            print('Test Fail.',format(e))

    def test_edu_studycenter_03(self):
        """学习记录"""
        lg = LoginPage(self.driver)
        ld = StudyCenterPage(self.driver)
        ld.get_url(ld.env.getUrl() + "/center/course/user/get-study-course")
        time.sleep(2)
        lg.close_focus_pop()
        ld.study_record_method()
        text1 = ld.study_record_text_method()
        text2 = ld.lesson_title_method()
        try:
            self.assertEqual(text1,u'学习记录',msg="学习记录加载成功")
            print('Test Pass.',"学习记录加载成功")
        except Exception as e:
            print('Test Fail.',format(e))
        ld.study_info_list_method()
        ld.switch_window()
        text3 = ld.play_lesson_title_method()
        try:
            self.assertIn(text2,text3,msg="课时名称一致")
            print('Test Pass.',"点击立即观看成功进入播放页面")
        except Exception as e:
            print('Test Fail.',format(e))

    def test_edu_studycenter_04(self):
        """笔记"""
        ld = StudyCenterPage(self.driver)
        ld.get_url(ld.env.getUrl() + "/center/course/user/get-study-course")
        ld.note_method()
        text1 = ld.note_tips_method()
        try:
            assert u'来到51CTO学院的' in text1
            print('Test Pass.', "访问笔记页面成功")
        except Exception as e:
            print('Test Fail.', format(e))

    def test_edu_studycenter_05(self):
        """我的提问"""
        lg = LoginPage(self.driver)
        ld = StudyCenterPage(self.driver)
        ld.get_url(ld.env.getUrl() + "/center/course/user/get-study-course")
        lg.close_focus_pop()
        ld.question_method()
        text1 = ld.my_question_method()
        text2 = ld.my_answer_method()
        text3 = ld.my_wejob_question_method()
        text4 = ld.question_tips_method()
        try:
            self.assertEqual(text1, u'我的提问', msg="我的提问加载成功")
            self.assertEqual(text2, u'我的回复',msg="我的回复加载成功")
            self.assertEqual(text3, u'我的微职位问答',msg="我的微职位问答加载成功")
            assert u'来到51CTO学院的' in text4
            print('Test Pass.', "访问笔记页面成功")
        except Exception as e:
            print('Test Fail.', format(e))

    def test_edu_studycenter_06(self):
        """学习打卡"""
        ld = StudyCenterPage(self.driver)
        ld.get_url(ld.env.getUrl() + "/center/course/user/get-study-course")
        ld.study_sign_card_method()
        ld.kown_method()
        text1 = ld.daliy_tasks_method()
        text2 = ld.sign_record_method()
        try:
            self.assertEqual(text1, u'每日任务', msg="每日任务加载成功")
            self.assertEqual(text2, u'为什么打卡',msg="打卡记录加载成功")
            print('Test Pass.', "访问学习打卡页面成功")
        except Exception as e:
            print('Test Fail.', format(e))


    def test_edu_studycenter_07(self):
        """我的题库"""
        ld = StudyCenterPage(self.driver)
        ld.get_url(ld.env.getUrl() + "/center/course/user/get-study-course")
        ld.exam_method()
        ld.switch_window()
        text1 = ld.my_exam_method()
        text2 = ld.my_error_method()
        try:
            self.assertEqual(text1, u'我的试卷', msg="我的试卷加载成功")
            self.assertEqual(text2, u'我的纠错',msg="我的纠错加载成功")
            print('Test Pass.', "访问我的题库页面成功")
        except Exception as e:
            print('Test Fail.', format(e))



    def test_edu_studycenter_08(self):
        """个人中心"""
        ld = StudyCenterPage(self.driver)
        time.sleep(2)
        ld.get_url(ld.env.getUrl() + "/center/user/info/get-user-info")
        time.sleep(2)

        text1 = ld.geren_method()
        text2 = ld.ziliao_method()
        try:
            self.assertEqual(text1,u"基本信息",msg="成功进入个人信息页")
            self.assertEqual(text2,u"学习档案",msg="成功进入个人信息页")
            print('Test Pass')
        except Exception as e:
            print('Test Fail',format(e))

    def test_edu_studycenter_09(self):
        """编辑个人信息"""
        lg = LoginPage(self.driver)
        ld = StudyCenterPage(self.driver)
        lg.close_focus_pop()
        time.sleep(2)
        ld.scroolbar_height()
        ld.edit_info_click()
        time.sleep(1)
        ld.edit_info_sendkeys('111111')
        qq_info_before = ld.qq_info_edit_method()
        ld.edit_save_click()
        self.driver.refresh()
        qq_info_after = ld.qq_info_metod()
        try:
            self.assertEqual(qq_info_before,qq_info_after,msg="qq信息同步成功")
            print('Test pass')
        except Exception as e:
            print('Test Fail',format(e))

    def test_edu_studycenter_10(self):
        """我的优惠券"""
        lg = LoginPage(self.driver)
        ld = StudyCenterPage(self.driver)
        ld.get_url(ld.env.getUrl() + "/center/user/info/get-user-info")
        time.sleep(1)
        lg.close_focus_pop()
        ld.edit_coupon_method()
        text1 = ld.coupon_info_method()
        try:
            assert text1 == u'优惠券激活'
            print('Test Pass')
        except Exception as e:
            print('Test Fail.', format(e))

    def test_edu_studycenter_11(self):
        """购买记录"""
        lg = LoginPage(self.driver)
        ld = StudyCenterPage(self.driver)
        ld.get_url(ld.env.getUrl() + "/center/user/info/get-user-info")
        time.sleep(1)
        lg.close_focus_pop()
        ld.get_order_list_method()
        text1 = ld.get_invoice_btn_method()
        try:
            assert text1 == u'开发票申请'
            print('Test Pass')
        except Exception as e:
            print('Test Fail.', format(e))
        time.sleep(2)
        ld.invoice_btn_click_method()
        try:
            assert u'添加发票_51CTO学院' in ld.get_page_title()
            print('Test Pass.')
        except Exception as e:
            print('Test Fail.',format(e))


if __name__ == '__main__ ':
    unittest.main()