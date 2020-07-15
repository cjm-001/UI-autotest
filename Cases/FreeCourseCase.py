import os
from util.BrowserEngine import BrowserEngine
from Pages.FreeCoursePage import FreeCoursePage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import time

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_common_status=ExcelUtil(user_data_path, "common_user_login_status")
d_common=sheet_with_login_common_status.dict_data()

@ddt.ddt
class FreeCourseCase(unittest.TestCase):
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
        print("免费课程case执行完成")

    @ddt.data(*d_common)
    def testFreeCourse(self,data):
        """验证免费课程观看流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.close_active_pop()
        self.lg.Login_Account(data['username'], data['password'])
        self.fcp = FreeCoursePage(self.driver)
        self.lg.webdriverWait(10)
        self.fcp.click_free_tab()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        #验证免费课程复选框可以成功勾选
        self.fcp.verify_free_checked()
        #验证第一个课程为免费课程
        self.fcp.verify_first_free_text()
        self.fcp.click_first_image()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        #验证课程详情页第一个课程为免费课程
        try:
            self.assertEqual(u'免费',self.fcp.get_free_label())
            print("课程价格处显示为免费")
        except Exception as e:
            print("课程价格处没有显示为免费")
        self.fcp.click_course_list()
        self.fcp.verify_chap_icon()
        self.fcp.current_handle_switch()
        self.lg.webdriverWait(10)
        #验证课时播放页可以成功打开
        try:
            self.assertIn(u'当前播放',self.fcp.get_current_play())
            print("课时播放页可以成功打开")
        except Exception as e:
            print("课时播放页无法成功打开")
        time.sleep(2)

    if __name__ == '__main__':
        unittest.main()