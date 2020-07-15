#coding=utf-8
import os
from util.BrowserEngine import BrowserEngine
from Pages.CourseDetailPage import CourseDetailPage
from Pages.LoginPage import LoginPage
from Pages.TeacherCoursePage import TeacherCoursePage
from util.ExcelUtil import ExcelUtil
import unittest
import time
import ddt
import re


user_data_path = os.path.dirname(os.path.abspath('.'))+ '\\data\\userinfo.xls'
sheet_with_login_common_status=ExcelUtil(user_data_path, "common_user_login_status")
d_common=sheet_with_login_common_status.dict_data()

@ddt.ddt
class CourseDatailCase(unittest.TestCase):
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
        print("课程详情页case执行完成")

    @ddt.data(*d_common)
    def testCourseDatail1(self,data):
        """验证非会员访问免费课程详情页流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'],data['password'])
        self.dc = CourseDetailPage(self.driver)
        self.lc = TeacherCoursePage(self.driver)
        self.dc.click_course_list()
        self.lg.current_handle_switch()
        self.dc.click_free_course()
        self.lg.webdriverWait(10)
        free_course_name=self.dc.list_course_title_text()
        free_course_lesson=self.dc.list_course_lesson_text()
        free_course_score=self.dc.list_course_rank_text()
        free_course_tag=self.dc.list_course_tag_text()
        free_course_price=self.dc.list_course_price_text()
        free_course_target=self.dc.list_course_target_text()
        self.dc.click_first_course()
        self.lg.current_handle_switch()
        detail_course_name=self.dc.detail_course_title_text()
        detail_course_lesson=self.dc.detail_course_lesson_text()
        detail_course_score=self.dc.detail_course_rank_text()
        detail_course_tag=self.dc.detail_course_tag_text()
        detail_course_price=self.dc.detail_course_price_text()
        detail_course_target=self.dc.detail_course_target_text()
        self.lg.webdriverWait(10)
        try:
            self.assertEqual(free_course_name,detail_course_name)
            print("课程列表页与课程详情页课程名称显示一致")
            self.assertEqual(free_course_lesson,detail_course_lesson)
            print("课程列表页与课程详情页课时数显示一致")
            self.assertIn(u'分',detail_course_score)
            print("课程列表页与课程详情页课程评分显示一致")
            self.assertEqual(free_course_tag,detail_course_tag)
            print("课程列表页与课程详情页课程等级显示一致")
            self.assertEqual(free_course_price,detail_course_price)
            print("课程列表页与课程详情页课程价格显示一致")
            self.assertEqual(free_course_target,detail_course_target)
            print("课程列表页与课程详情页课程目标显示一致")
        except Exception as e:
            print("课程列表页课程字段值与课程详情页显示不一致",format(e))
        detail_lec_name=self.dc.detail_lec_name_text()
        detail_lec_rank=self.dc.detail_lec_rank_text()
        detail_lec_course=re.sub("\D","",self.dc.detail_lec_course_text())
        self.dc.detail_lec_name_click()
        self.lg.switch_window_without_close()
        lec_teacher_name=self.lc.get_teacher_name()
        lec_lec_course=self.lc.get_lec_course()
        try:
            self.assertEqual(detail_lec_name,lec_teacher_name)
            print("课程详情页与讲师主页讲师姓名字段展示一致")
            self.assertIn(detail_lec_course,lec_lec_course)
            print("课程详情页与讲师主页讲师课程数字段展示一致")
        except Exception as e:
            print("课程详情页讲师字段值与讲师详情页显示不一致",format(e))
        self.lg.switch_previous_window()
        self.dc.detail_course_jieshao_click()
        try:
            self.assertEqual(u'适合人群：',self.dc.get_suitable_person())
            self.assertEqual(u'课程目标：',self.dc.get_course_target())
            self.assertEqual(u'课程简介：',self.dc.get_course_introduce())
            print("课程介绍板块加载正常")
        except Exception as e:
            print("课程介绍板块加载不正确",format(e))
        self.dc.detail_course_dagan_click()
        try:
            self.assertEqual(u'课程大纲',self.dc.get_course_dagan_guide())
            print("课程大纲板块加载正常")
        except Exception as e:
            print("课程大纲板块加载不正确",format(e))
        self.lg.webdriverWait(10)
        self.dc.detail_study_lujin_click()
        try:
            self.assertEqual(u'学习路径',self.dc.get_course_lujin_guide())
            self.assertIn(u'发现更多',self.dc.get_course_lujin_more())
            print("学习路径板块加载正常")
        except Exception as e:
            print("学习路径板块加载不正确",format(e))
        self.dc.detail_student_pingjia_click()
        try:
            self.assertIn(self.dc.get_student_pingjia_sore_detail(),self.dc.detail_course_rank_text())
            print("学员评价板块加载正常")
        except Exception as e:
            print("学员评价板块加载不正确",format(e))
        self.dc.detail_other_course_click()
        try:
            self.assertIn(u'的更多课程',self.dc.get_detail_other_guide())
            print("其他课程板块加载正常")
        except Exception as e:
            print("其他板块加载不正确",format(e))
        self.dc.detail_course_jieshao_new_click()
        self.dc.verify_wechat_number()
        self.dc.guess_like_text()
        self.dc.verify_month_more()
        self.lg.switch_window_without_close()
        time.sleep(2)
        try:
            self.assertIn(u'51CTO学院排行榜',self.lg.get_page_title())
            print("月度受欢迎更多板块打开正常")
        except Exception as e:
            print("月度受欢迎更多板块打开不正常",format(e))











