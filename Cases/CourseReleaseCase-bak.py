# coding=utf-8
import unittest
import time
import ddt
import os.path
from util.ExcelUtil import ExcelUtil
from Pages.CourseReleasePage import CourseReleasePage
from Pages.LoginPage import LoginPage
from util.BrowserEngine import BrowserEngine

dir = os.path.dirname(os.path.abspath('.'))
img_path = os.path.abspath(dir + '/img/001.jpg')
upfile_path = os.path.abspath(dir + '/util/upfile.exe')
video_path = os.path.abspath(dir + '/img/testvideo.mp4')
file_path = dir + '/data/userinfo.xls'
sheet5Name = "lecture"
data1 = ExcelUtil(file_path, sheet5Name)
lectureData = data1.dict_data()


@ddt.ddt
class CourseReleaseCase(unittest.TestCase):
    def setUp(self):
        browse = BrowserEngine(self)
        self.driver = browse.open_browser(self)

    def tearDown(self):
        self.driver.quit()
        print("讲师发布课程case执行完成")

    @ddt.data(*lectureData)
    def test_course_creat_list(self,data1):
        """创建草稿课程"""
        self.homepage = LoginPage(self.driver)
        self.homepage.Login_Account(data1["username"], data1["password"])
        self.ld = CourseReleasePage(self.driver)
        self.driver.get(self.ld.env.getUrl())
        self.ld.lecture_center_method()
        text1 = self.ld.course_method()
        text2 = self.ld.review_course_method()
        try:
            assert u'已发布的课程' in text1
            assert u'待发布的课程' in text2
            print('Test pass.',"成功进入课程管理页面")
        except Exception as e:
            print('Test Fali',format(e))
        self.ld.webdriverWait(10)
        self.ld.creatCourse_method()
        self.ld.switch_window()
        self.ld.course_title_method("自动化创建草稿测试课程")
        time.sleep(3)
        self.ld.Lv1_select_method()
        self.ld.Lv1_method()
        time.sleep(3)
        self.ld.Lv2_select_method()
        self.ld.Lv2_method()
        self.ld.course_target_method("学习您的课程后，学生能够实现或达成哪些目标？合理设置课程目标，加速学生决策，提升购买转化率")
        self.ld.for_who_method("开发、测试、运维")
        self.ld.scroolbar_height()
        self.ld.course_introduction_method("课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介")
        self.ld.course_tag_method("项目实战、机器学习")
        self.ld.img_Load_method(img_path)
        time.sleep(3)
        self.ld.save_btn_method()
        text3 = self.ld.cStepTitle_method()
        try:
            self.assertEqual(text3,u'创建课程大纲')
            print("Test pass.","成功进入创建课程大纲页面")
        except Exception as e:
            print("Test Fail.",format(e))
        self.ld.lesson_add_method()
        self.ld.title_method("软件测试第一课时")
        self.ld.describe_method("课时简介")
        self.ld.video_shangchuan_method()
        os.system(upfile_path + " " + video_path)
        time.sleep(5)
        self.ld.scroolbar_height()
        self.ld.save_lesson_method()
        time.sleep(3)
        self.ld.go_Next_method()
        text4 = self.ld.Notices_method()
        try:
            self.assertEqual(text4,u'课程创建成功，提交审核后我们将48小时内进行审核，审核结果将发送站内消息通知您，请及时关注')
            print('Test Pass.',"成功进入课程提交审核页面")
        except Exception as e:
            print('Test Fail.',format(e))
        self.ld.save_draft_method()
        self.ld.webdriverWait(10)
        text5 = self.ld.list_released_method()
        try:
            assert u'草稿' in text5
            print('Test Pass.',"待发布课程-草稿课程创建成功")
        except Exception as e:
            print('Test Fail.',format(e))
        self.ld.delete_course_method()
        time.sleep(2)
        self.ld.query_delete_course_method()


    # @ddt.data(*lectureData)
    # def course_creat_shenhe(self,data1):
    #     """创建待审核课程"""
    #     homepage = LoginPage(self.driver)
    #     homepage.Login_Account(data1["username"], data1["password"])
    #     ld = CourseReleasePage(self.driver)
    #     self.driver.get(ld.env.getUrl())
    #     ld.lecture_center_method()
    #     text1 = ld.course_method()
    #     text2 = ld.review_course_method()
    #     try:
    #         assert u'已发布的课程' in text1
    #         assert u'待发布的课程' in text2
    #         print('Test pass.',"成功进入课程管理页面")
    #     except Exception as e:
    #         print('Test Fali',format(e))
    #     ld.creatCourse_method()
    #     ld.switch_window()
    #     ld.course_title_method("自动化创建待审核测试课程")
    #     time.sleep(3)
    #     ld.Lv1_select_method()
    #     ld.Lv1_method()
    #     ld.Lv2_select_method()
    #     time.sleep(3)
    #     ld.Lv2_method()
    #     ld.course_target_method("学习您的课程后，学生能够实现或达成哪些目标？合理设置课程目标，加速学生决策，提升购买转化率")
    #     ld.for_who_method("开发、测试、运维")
    #     ld.course_introduction_method("课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介课程简介")
    #     ld.course_tag_method("项目实战、机器学习")
    #     ld.img_Load_method(img_path)
    #     time.sleep(3)
    #     ld.save_btn_method()
    #     text3 = ld.cStepTitle_method()
    #     try:
    #         self.assertEqual(text3,u'创建课程大纲')
    #         print("Test pass.","成功进入创建课程大纲页面")
    #     except Exception as e:
    #         print("Test Fail.",format(e))
    #     ld.lesson_add_method()
    #     ld.title_method("软件测试第一课时")
    #     ld.describe_method("课时简介")
    #     #ld.video_upload_method()
    #     ld.type_select_method()
    #     ld.content_method("说明类课时")
    #     ld.webdriverWait(10)
    #     ld.scroolbar_height()
    #     ld.save_lesson_method()
    #     time.sleep(3)
    #     ld.go_Next_method()
    #     text4 = ld.Notices_method()
    #     try:
    #         self.assertEqual(text4,u'课程创建成功，提交审核后我们将48小时内进行审核，审核结果将发送站内消息通知您，请及时关注')
    #         print('Test Pass.',"成功进入课程提交审核页面")
    #     except Exception as e:
    #         print('Test Fail.',format(e))
    #     ld.submit_audit_method()
    #     ld.webdriverWait(10)
    #     text5 = ld.list_released_method()
    #     try:
    #         assert u'待审核' in text5
    #         print('Test Pass.',"待发布课程-待发布课程创建成功")
    #     except Exception as e:
    #         print('Test Fail.',format(e))





if __name__ == '__main__':
    unittest.main()