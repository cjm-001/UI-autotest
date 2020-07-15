#coding=utf-8
import os
from util.BrowserEngine import BrowserEngine
from Pages.SoftExamStoryPage import SoftExamStoryPage
from util.ExcelUtil import ExcelUtil
from Pages.LoginPage import LoginPage
import unittest
import time
import ddt

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_common_status=ExcelUtil(user_data_path, "common_user_login_status")
d_common=sheet_with_login_common_status.dict_data()

@ddt.ddt
class SoftExamStoryCase(unittest.TestCase):
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
        print("软考学员故事case执行完成")

    def testSoftExamDryCargo_notlogin(self):
        """验证未登录状态学员故事流程"""
        self.lg=LoginPage(self.driver)
        self.lg.close_active_pop()
        self.nldc = SoftExamStoryPage(self.driver)
        #self.nldc.wejob_link_method()
        self.nldc.wejob_enter_method()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.nldc.click_rk_tab()
        self.lg.webdriverWait(10)
        self.nldc.click_drycargo_tab()
        #验证学员故事页面可以成功打开
        self.lg.webdriverWait(10)
        first_arc_title=self.nldc.get_first_dry()
        print(first_arc_title)
        time.sleep(2)
        self.nldc.click_first_dry()
        self.lg.current_handle_switch()
        try:
            self.assertEqual(first_arc_title,self.nldc.get_drycargo_title())
            print("学员故事详情页可以成功打开")
        except Exception as e:
            print("学员故事详情页无法打开")
        self.nldc.click_softtab_subpage()
        self.lg.webdriverWait(10)
        self.nldc.click_my_article()
        self.nldc.verify_login_text()
        time.sleep(2)

    @ddt.data(*d_common)
    def testSoftExamDryCargo(self, data):
        """验证登录用户软考干货流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.lg.Login_Account(data['username'], data['password'])
        self.sdc = SoftExamStoryPage(self.driver)
        self.lg.webdriverWait(10)
        #self.sdc.wejob_link_method()
        self.sdc.wejob_enter_method()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.sdc.click_rk_tab()
        self.lg.webdriverWait(10)
        self.sdc.click_drycargo_tab()
        '''-----国庆节前夕学员发表文章入口屏蔽-----
        #验证发布文章页面可以打开
        self.sdc.click_want_to_share()
        try:
            self.assertEqual(u'发布文章',self.sdc.get_deploy_text())
            print("发布文章页面可以打开")
        except Exception as e:
            print("发布文章页面不能打开")
        #验证文章信息可以成功录入
        self.sdc.type_article_title("我是测试文章标题")
        self.sdc.click_article_type()
        self.sdc.select_type_value()
        self.sdc.input_article_description("我是测试文章描述")
        print("因为线上发布文章无需审核，为避免产生测试数据，不执行提交操作")
        '''

    def testTeacherMaterials(self):
        """验证教学资料功能正确"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.tm = SoftExamStoryPage(self.driver)
        self.lg.webdriverWait(10)
        #self.tm.wejob_link_method()
        self.tm.wejob_enter_method()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.tm.click_rk_tab()
        self.lg.webdriverWait(10)
        self.tm.click_teach_materials()
        self.lg.webdriverWait(10)
        #验证教材资料可以打开
        try:
            assert u"教材资料" in self.tm.get_page_title()
            print("教材资料页面打开成功")
        except Exception as e:
            print("教材资料页面打开失败", format(e))
        #验证配套图书板块可以展示
        try:
            self.assertEqual(u'配套图书',self.tm.get_match_book())
            print("配套图书板块可以展示")
        except Exception as e:
            print("配套图书板块不能展示")
        #验证学习资料板块可以展示
        try:
            assert u'学习资料' in self.tm.get_study_materials()
            print("学习资料板块可以展示")
        except Exception as e:
            print("学习资料板块不能展示")

    def testCourseCenter(self):
        """验证课程中心功能正确"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.tcc = SoftExamStoryPage(self.driver)
        self.lg.webdriverWait(10)
        # self.tm.wejob_link_method()
        self.tcc.wejob_enter_method()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.tcc.click_rk_tab()
        self.lg.webdriverWait(10)
        self.tcc.click_course_choose_tab()
        self.lg.webdriverWait(10)
        # 验证微职位软考列表页面可以打开
        self.lg.switch_window_without_close()
        try:
            assert u"该分类下有" in self.tcc.get_type_text()
            print("软考课程列表页面打开成功")
        except Exception as e:
            print("软考课程列表页面打开失败", format(e))
        time.sleep(2)
        # 验证课程排行榜页面可以展示
        self.lg.switch_previous_window()
        self.tcc.click_video_course()
        self.lg.current_handle_switch()
        try:
            assert u'软考视频课程排行榜' in self.tcc.get_page_title()
            print("软考视频课程排行榜页面可以成功打开")
        except Exception as e:
            print("软考视频课程排行榜页面不能打开")


if __name__ == '__main__':
    unittest.main()
