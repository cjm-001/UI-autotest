import os
from util.BrowserEngine import BrowserEngine
from Pages.CourseCreatePage import CourseCreatePage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import time

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_vip_status = ExcelUtil(user_data_path, "lecture")
d_lec = sheet_with_login_vip_status.dict_data()
course_pic_path=os.path.dirname(os.path.abspath('.'))+'\\img\\course_001.jpg'
uptool_path=os.path.dirname(os.path.abspath('.'))+'\\util\\upfile.exe'
course_video_path=os.path.dirname(os.path.abspath('.'))+'\\img\\testvideo.mp4'


@ddt.ddt
class CourseCreateCase(unittest.TestCase):
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
        print("讲师创建课程case执行完成")

    @ddt.data(*d_lec)
    def testTeacherCreateCourse(self,data):
        """验证讲师创建课程流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'], data['password'])
        self.cc = CourseCreatePage(self.driver)
        self.cc.click_createcourse()
        time.sleep(2)
        self.lg.current_handle_switch()
        self.lg.close_teach_notice_pop()
        self.cc.click_createCourse_button()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        # 验证课程创建页面能够成功打开
        try:
            assert u'发布新课程'==self.cc.get_first_create_page()
            print("课程创建页面可以成功打开")
        except Exception as e:
            print("课程创建页面不能成功打开",format(e))
        self.cc.course_title_enter("这是一个测试课程标题，请勿审核通过~这是一个测试课程标题，请勿审核通过~")
        time.sleep(2)
        self.cc.click_first_class()
        time.sleep(2)
        self.cc.select_first_class()
        time.sleep(1)
        self.cc.click_second_class()
        self.cc.select_second_class()
        self.cc.select_diff2()
        time.sleep(2)
        self.cc.input_course_revenue("测试测试")
        self.cc.click_course_revenue()
        self.cc.input_suitable_people("适合人群测试数据")
        self.cc.input_study_plan("学习计划")
        self.cc.input_course_target("课程目标测试课程目标测试课程目标测试课程目标测试")
        #self.cc.input_for_who("测试学群测试学习人群测试学习人群测试")
        self.cc.scroolbar_height()
        self.cc.input_course_description("课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介")
        self.lg.webdriverWait(10)
        self.cc.input_tag("测试课程标签1,测试课程标签2,测试课程标签3,测试课程标签4,测试课程标签5")
        self.cc.upload_pic(course_pic_path)
        self.lg.webdriverWait(10)
        self.cc.scroolbar_height()
        self.cc.click_course_type()
        time.sleep(3)
        self.cc.click_first_save()
        self.lg.webdriverWait(10)
        #验证创建课程大纲流程正确
        try:
            assert u'创建课程大纲'==self.cc.get_second_title()
            print("创建课程大纲页面可以正常打开")
        except Exception as e:
            print("创建课程大纲不能成功打开",format(e))
        self.lg.webdriverWait(10)
        self.cc.click_add_chapter()
        self.cc.type_first_chap("这是第一测试章节")
        self.cc.click_charp_save()
        time.sleep(2)
        #直接创建单页类型课时
        self.cc.click_add_less()
        self.cc.type_less_title("这是一个单页类型测试课时标题")
        self.cc.type_less_des("这是一个单页类型测试课时简介")
        self.cc.select_less_des_type()
        time.sleep(2)
        self.cc.input_lesson_description("这是一个单页类型的课时内容")
        self.cc.click_lesson2_save()
        time.sleep(2)
        self.cc.scroolbar_height()
        self.cc.click_new_button()
        self.lg.webdriverWait(10)
        '''
        #创建视频类型课时
        self.cc.click_add_less()
        self.cc.type_less_title("这是一个视频类型测试课时标题")
        self.cc.type_less_des("这是一个视频类型测试课时简介")
        time.sleep(2)
        self.cc.click_upload_video()
        os.system(uptool_path+" "+ course_video_path)
        time.sleep(5)
        self.cc.scroolbar_height()
        self.cc.click_less_save()
        time.sleep(2)
        self.cc.scroolbar_height()
        
        #创建单页类型课时
        self.cc.click_add_lesson_two()
        self.cc.type_less2_title("这是一个单页类型测试课时标题")
        self.cc.type_less2_des("这是一个单页类型测试课时简介")
        self.cc.select_less_des_type()
        time.sleep(2)
        self.cc.input_lesson_description("这是一个单页类型的课时内容")
        self.cc.click_lesson2_save()
        time.sleep(2)
        self.cc.scroolbar_height()
        self.cc.click_new_button()
        self.lg.webdriverWait(10)
        '''
        # 验证创建课程大纲流程正确
        try:
            assert u'提交审核' == self.cc.get_audit_text()
            print("提交审核页面可以正常打开")
        except Exception as e:
            print("提交审核页面不能成功打开", format(e))
        self.cc.click_save_draft()
        self.lg.webdriverWait(10)
        # 验证课程草稿状态正确
        try:
            assert u'草稿' in self.cc.get_draft_status()
            print("课程为草稿状态")
        except Exception as e:
            print("课程不是草稿状态，获取状态不正确", format(e))
        time.sleep(2)
        #删除草稿状态课程，实现数据初始化
        self.cc.click_delete_course()
        self.lg.webdriverWait(10)
        self.cc.click_delete_button()
        time.sleep(2)


if __name__ == '__main__':
    unittest.main()