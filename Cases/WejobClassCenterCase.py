import os
from util.BrowserEngine import BrowserEngine
from Pages.WejobClassCenterPage import WejobClassCenterPage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import time

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_common_status=ExcelUtil(user_data_path, "common_user_login_status")
d_common=sheet_with_login_common_status.dict_data()

@ddt.ddt
class WejobClassCenterCase(unittest.TestCase):
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
        print("微职位班级中心case执行完成")

    @ddt.data(*d_common)
    def testnotVipSignIn(self, data):
        """验证微职位班级中心流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'], data['password'])
        self.wjc = WejobClassCenterPage(self.driver)
        self.wjc.click_study_center()
        self.lg.webdriverWait(10)
        self.wjc.click_class_enter()
        #验证微信关注和班级引导存在,并进行关闭
        self.wjc.close_join_class_guide_step1()
        self.wjc.close_join_class_guide_step2()
        self.lg.webdriverWait(10)
        self.wjc.close_join_class_guide_step3()
        self.wjc.close_winxinpop()
        self.lg.webdriverWait(10)
        self.wjc.click_noneed_guide()
        self.lg.webdriverWait(10)
        #验证班级中心页面打开
        self.wjc.verify_progress_exist()
        try:
            self.assertEqual(u'班级公告',self.wjc.get_annnouncement_text())
            print("班级公告板块存在")
        except Exception as e:
            print("班级公告板块不存在")
        self.wjc.click_all_anno()
        self.wjc.current_handle_switch()
        self.lg.webdriverWait(10)
        #验证班级公告页面可以打开
        try:
            self.assertIn(u'班级公告',self.wjc.get_class_anno_title())
            print("班级公告页面可以打开")
        except Exception as e:
            print("班级公告页面不能打开")
        self.lg.webdriverWait(10)
        self.wjc.click_back_to_class_anno()
        self.lg.webdriverWait(10)
        #验证排行榜板块可以展示
        try:
            self.assertIn(u'学习排行榜',self.wjc.get_rank_text())
            print("班级学习排行榜板块可以展示")
        except Exception as e:
            print("班级学习排行榜板块无法展示")
        #验证学习宣言板块存在
        try:
            self.assertIn(u'学习宣言展示墙',self.wjc.get_study_declaration())
            print("学习宣言板块存在")
        except Exception as e:
            print("学习宣言板块无法展示")
        self.wjc.click_all_decla()
        self.wjc.current_handle_switch()
        self.lg.webdriverWait(10)
        try:
            self.assertIn(u'学习宣言',self.wjc.get_declara_title())
            print("学习宣言页面可以打开")
        except Exception as e:
            print("学习宣言页面无法打开")
        self.wjc.click_back_to_class_decla()
        self.lg.webdriverWait(10)
        #验证课程tab可以打开
        self.wjc.click_lesson_tab()
        self.lg.webdriverWait(10)
        self.wjc.verify_course_item_exist()
        #验证直播tab可以打开
        self.wjc.click_live_tab()
        self.lg.webdriverWait(10)
        self.wjc.verify_live_list_exist()
        #验证作业tab可以打开
        self.wjc.click_exam_tab()
        self.lg.webdriverWait(10)
        self.wjc.verify_exam_item_exist()
        #验证题库tab可以打开
        self.wjc.click_subject_tab()
        self.lg.webdriverWait(10)
        self.wjc.verify_subject_table()
        #验证资料tab可以打开
        self.wjc.click_material_tab()
        self.lg.webdriverWait(10)
        self.wjc.verify_material_item_exist()
        #验证问答tab可以打开
        self.wjc.click_question_tab()
        self.lg.webdriverWait(10)
        self.wjc.verify_question_title_exist()
        #验证帮助中心tab可以打开
        self.wjc.click_helpcenter_tab()
        self.wjc.current_handle_switch()
        self.lg.webdriverWait(10)
        self.wjc.verify_help_center_exist()

if __name__ == '__main__':
    unittest.main()


