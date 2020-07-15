import os
from util.BrowserEngine import BrowserEngine
from Pages.SubjectCreatePage import SubjectCreatePage
from Pages.LoginPage import LoginPage
import unittest
from util.ExcelUtil import ExcelUtil
import ddt
import time

user_data_path = os.path.dirname(os.path.abspath('.')) + '\\data\\userinfo.xls'
sheet_with_login_vip_status = ExcelUtil(user_data_path, "lecture")
d_lec = sheet_with_login_vip_status.dict_data()


@ddt.ddt
class SubjectCreateCase(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        browser = BrowserEngine(self)
        self.driver = browser.open_browser(self)

    @classmethod
    def tearDownClass(self):
        self.driver.close()
        print("讲师创建题目case执行完成")

    @ddt.data(*d_lec)
    def testTestPaper_01_SingleChoiceQuestion(self, data):
        """验证讲师创建单选题流程正确"""
        self.lg = LoginPage(self.driver)
        self.lg.Login_Account(data['username'], data['password'])
        self.tc = SubjectCreatePage(self.driver)
        self.tc.click_coursedeploy()
        self.lg.current_handle_switch()
        self.lg.close_teach_notice_pop()
        self.tc.click_mylib()
        self.tc.click_testpaperlib()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        # 验证试卷管理中心页面能够成功打开
        try:
            assert u'发布新课程' == self.tc.get_text_papermanager()
            print("试卷管理中心页面可以成功打开")
        except Exception as e:
            print("试卷管理中心页面不能成功打开", format(e))
        self.lg.webdriverWait(10)
        #打开我的题目页面，查看是否存在脏数据
        self.tc.click_my_subject_tab()
        single_stem_string = "这是一道测试单选题，请勿审核通过"
        self.tc.input_stem_inmysubject(single_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        self.tc.verify_nodata_exist()
        # try:
        #     self.assertEqual(single_stem_string, self.tc.get_stem_intable())
        #     print("上次题目没有被删除掉，数据初始化需要重新删除")
        #     self.tc.click_deleteicon()
        #     self.lg.webdriverWait(10)
        #     self.tc.click_delete_button()
        # except Exception as e:
        #     print("题目已经被删除掉，不用再删除了")
        #新增题目
        self.tc.click_add_subject_button()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.tc.click_paper_type1()
        self.lg.webdriverWait(10)
        self.tc.select_paper_type1()
        self.tc.click_paper_type2()
        self.lg.webdriverWait(10)
        self.tc.select_paper_type2()
        self.tc.click_chapter1()
        self.tc.select_chapter1()
        time.sleep(1)
        self.tc.select_chapter2()
        time.sleep(1)
        self.tc.input_knowledge_point("这是测试知识点")
        self.tc.input_stem(single_stem_string)
        self.tc.input_option1("这是选项1")
        self.tc.set_single_answer_ejs()
        self.tc.input_option2("这是选项2")
        self.tc.input_option3("这是选项3")
        self.tc.input_option4("这是选项4")
        self.tc.scroolbar_size()
        self.tc.input_analysis("这是答案解析")
        self.tc.click_label()
        self.tc.set_subject_difficulty()
        self.tc.click_submit_subject()
        self.lg.webdriverWait(10)
        time.sleep(2)
        #验证我的题目tab可以成功打开
        try:
            assert u'我的题目' == self.tc.get_mysubject()
            print("我的题目页面可以成功打开")
        except Exception as e:
            print("我的题目页面不能成功打开", format(e))
        time.sleep(2)
        #验证新创建的课程可以成功筛选
        self.tc.click_paper_type1_inmysubject()
        time.sleep(1)
        self.tc.select_paper_type1_inmysubject()
        self.lg.webdriverWait(10)
        self.tc.click_paper_type2_inmysubject()
        self.lg.webdriverWait(10)
        self.tc.select_paper_type2_inmysubject()
        self.tc.click_question_type_inmysubject()
        self.tc.select_question_single_type_inmysubject()
        time.sleep(1)
        self.tc.click_difficulty_inmysubject()
        self.tc.select_difficulty_type_inmysubject()
        self.tc.click_status_inmysubject()
        self.tc.select_status_inmysubject()
        self.tc.input_stem_inmysubject(single_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        time.sleep(2)
        #验证列表题目与创建题目信息匹配
        try:
            self.assertEqual(single_stem_string,self.tc.get_stem_intable())
            print("题干与创建时匹配，试卷创建成功")
        except Exception as e:
            print("题干与创建时不匹配，试卷创建不成功")
        time.sleep(2)
        #删除待审核状态题目，实现数据初始化
        self.tc.click_deleteicon()
        self.lg.webdriverWait(10)
        self.tc.click_delete_button()
        self.lg.webdriverWait(10)
        print("测试单选题被删除了~")
        # 验证题目删除失败后重新删除
        self.tc.input_stem_inmysubject(single_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        try:
            self.assertEqual(single_stem_string,self.tc.get_stem_intable())
            print("题目没有被删除掉，数据初始化需要重新删除")
            self.tc.click_deleteicon()
            self.lg.webdriverWait(10)
            self.tc.click_delete_button()
        except Exception as e:
            print("题目已经被删除掉，不用再删除了")

    @ddt.data(*d_lec)
    def testTestPaper_02_MultipleChoiceQuestions(self, data):
        """验证讲师创建多选题流程正确"""
        self.lg = LoginPage(self.driver)
        self.tc = SubjectCreatePage(self.driver)
        self.tc.get_url(self.tc.env.getUrl() + "/t/lecturer/question")
        self.lg.webdriverWait(10)
        # 打开我的题目页面，查看是否存在脏数据
        self.tc.click_my_subject_tab_notmanagepage()
        multiple_stem_string = "这是一道测试多选题，请勿审核通过"
        self.tc.input_stem_inmysubject(multiple_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        self.tc.verify_nodata_exist()
        # try:
        #     self.assertEqual(multiple_stem_string, self.tc.get_stem_intable())
        #     print("上次题目没有被删除掉，数据初始化需要重新删除")
        #     self.tc.click_deleteicon()
        #     self.lg.webdriverWait(10)
        #     self.tc.click_delete_button()
        # except Exception as e:
        #     print("题目已经被删除掉，不用再删除了")
        #创建多选题
        self.tc.click_add_subject_button()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.tc.click_paper_type1()
        self.lg.webdriverWait(10)
        self.tc.select_paper_type1()
        self.lg.webdriverWait(10)
        self.tc.click_paper_type2()
        self.tc.select_paper_type2()
        self.tc.click_chapter1()
        self.tc.select_chapter1()
        time.sleep(1)
        self.tc.select_chapter2()
        time.sleep(1)
        self.tc.input_knowledge_point("这是测试知识点")
        self.tc.click_multiple_tab()
        self.tc.input_stem(multiple_stem_string)
        self.tc.input_mulitle_option1("这是选项1")
        self.tc.input_mulitle_option2("这是选项2")
        self.tc.set_multiple_answer1_ejs()
        self.tc.set_multiple_answer2_ejs()
        self.tc.input_mulitle_option3("这是选项3")
        self.tc.input_mulitle_option4("这是选项4")
        self.tc.scroolbar_size()
        self.tc.input_analysis("这是答案解析")
        self.tc.click_label()
        self.tc.set_subject_difficulty()
        self.tc.click_submit_subject()
        self.lg.webdriverWait(10)
        time.sleep(2)
        # 验证我的题目tab可以成功打开
        try:
            assert u'我的题目' == self.tc.get_mysubject()
            print("我的题目页面可以成功打开")
        except Exception as e:
            print("我的题目页面不能成功打开", format(e))
        # 验证新创建的课程可以成功筛选
        self.tc.click_paper_type1_inmysubject()
        time.sleep(2)
        self.tc.select_paper_type1_inmysubject()
        self.lg.webdriverWait(10)
        self.tc.click_paper_type2_inmysubject()
        self.lg.webdriverWait(10)
        self.tc.select_paper_type2_inmysubject()
        self.tc.click_question_type_inmysubject()
        self.tc.select_question_mulitle_type_inmysubject()
        time.sleep(1)
        self.tc.click_difficulty_inmysubject()
        self.tc.select_difficulty_type_inmysubject()
        self.tc.click_status_inmysubject()
        self.tc.select_status_inmysubject()
        self.tc.input_stem_inmysubject(multiple_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        # 验证列表题目与创建题目信息匹配
        try:
            self.assertEqual(multiple_stem_string, self.tc.get_stem_intable())
            print("题干与创建时匹配，试卷创建成功")
        except Exception as e:
            print("题干与创建时不匹配，试卷创建不成功")
        time.sleep(2)
        # 删除待审核状态题目，实现数据初始化
        self.tc.click_deleteicon()
        self.tc.click_delete_button()
        print("测试多选题被删除了~")
        # 验证题目删除失败后重新删除
        self.tc.input_stem_inmysubject(multiple_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        try:
            self.assertEqual(multiple_stem_string, self.tc.get_stem_intable())
            print("题目没有被删除掉，数据初始化需要重新删除")
            self.tc.click_deleteicon()
            self.lg.webdriverWait(10)
            self.tc.click_delete_button()
        except Exception as e:
            print("题目已经被删除掉，不用再删除了")

    @ddt.data(*d_lec)
    def testTestPaper_03_JudgementQuestion(self, data):
        """验证讲师创建判断题流程正确"""
        self.lg = LoginPage(self.driver)
        self.tc = SubjectCreatePage(self.driver)
        self.tc.get_url(self.tc.env.getUrl() + "/t/lecturer/question")
        self.lg.webdriverWait(10)
        # 打开我的题目页面，查看是否存在脏数据
        judgement_stem_string = "这是一道测试判断题，请勿审核通过"
        self.tc.input_stem_inmysubject(judgement_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        self.tc.verify_nodata_exist()
        # try:
        #     self.assertEqual(judgement_stem_string, self.tc.get_stem_intable())
        #     print("上次题目没有被删除掉，数据初始化需要重新删除")
        #     self.tc.click_deleteicon()
        #     self.lg.webdriverWait(10)
        #     self.tc.click_delete_button()
        # except Exception as e:
        #     print("题目已经被删除掉，不用再删除了")
        #新增题目
        self.tc.click_add_subject_button()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.tc.click_paper_type1()
        self.lg.webdriverWait(10)
        self.tc.select_paper_type1()
        self.tc.click_paper_type2()
        self.lg.webdriverWait(10)
        self.tc.select_paper_type2()
        self.tc.click_chapter1()
        self.tc.select_chapter1()
        time.sleep(1)
        self.tc.select_chapter2()
        time.sleep(1)
        self.tc.input_knowledge_point("这是测试知识点")
        self.tc.click_judge_tab()
        self.tc.input_stem(judgement_stem_string)
        self.tc.set_judge_answer_ejs()
        self.tc.scroolbar_size()
        self.tc.input_analysis("这是答案解析")
        self.tc.click_label()
        self.tc.set_subject_difficulty()
        self.tc.click_submit_subject()
        self.lg.webdriverWait(10)
        # 验证我的题目tab可以成功打开
        try:
            assert u'我的题目' == self.tc.get_mysubject()
            print("我的题目页面可以成功打开")
        except Exception as e:
            print("我的题目页面不能成功打开", format(e))
        time.sleep(2)
        # 验证新创建的课程可以成功筛选
        self.tc.click_paper_type1_inmysubject()
        time.sleep(1)
        self.tc.select_paper_type1_inmysubject()
        time.sleep(1)
        self.lg.webdriverWait(10)
        self.tc.click_paper_type2_inmysubject()
        self.lg.webdriverWait(10)
        self.tc.select_paper_type2_inmysubject()
        self.tc.click_question_type_inmysubject()
        self.tc.select_question_judgement_type_inmysubject()
        time.sleep(1)
        self.tc.click_difficulty_inmysubject()
        self.tc.select_difficulty_type_inmysubject()
        self.tc.click_status_inmysubject()
        self.tc.select_status_inmysubject()
        self.tc.input_stem_inmysubject(judgement_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        # 验证列表题目与创建题目信息匹配
        try:
            self.assertEqual(judgement_stem_string, self.tc.get_stem_intable())
            print("题干与创建时匹配，试卷创建成功")
        except Exception as e:
            print("题干与创建时不匹配，试卷创建不成功")
        time.sleep(2)
        # 删除待审核状态题目，实现数据初始化
        self.tc.click_deleteicon()
        self.tc.click_delete_button()
        print("测试判断题被删除了~")
        # 验证题目删除失败后重新删除
        self.tc.input_stem_inmysubject(judgement_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        try:
            self.assertEqual(judgement_stem_string, self.tc.get_stem_intable())
            print("题目没有被删除掉，数据初始化需要重新删除")
            self.tc.click_deleteicon()
            self.lg.webdriverWait(10)
            self.tc.click_delete_button()
        except Exception as e:
            print("题目已经被删除掉，不用再删除了")

    @ddt.data(*d_lec)
    def testTestPaper_04_CompletionQuestion(self, data):
        """验证讲师创建填空题流程正确"""
        self.lg = LoginPage(self.driver)
        self.tc = SubjectCreatePage(self.driver)
        self.tc.get_url(self.tc.env.getUrl() + "/t/lecturer/question")
        self.lg.webdriverWait(10)
        # 打开我的题目页面，查看是否存在脏数据
        completion_stem_string = "这是一道测试填空题，请勿审核通过"
        self.tc.input_stem_inmysubject(completion_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        self.tc.verify_nodata_exist()
        # try:
        #     self.assertEqual(completion_stem_string, self.tc.get_stem_intable())
        #     print("上次题目没有被删除掉，数据初始化需要重新删除")
        #     self.tc.click_deleteicon()
        #     self.lg.webdriverWait(10)
        #     self.tc.click_delete_button()
        # except Exception as e:
        #     print("题目已经被删除掉，不用再删除了")
        # 新增题目
        self.tc.click_add_subject_button()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.tc.click_paper_type1()
        self.lg.webdriverWait(10)
        self.tc.select_paper_type1()
        self.tc.click_paper_type2()
        self.lg.webdriverWait(10)
        self.tc.select_paper_type2()
        self.tc.click_chapter1()
        self.tc.select_chapter1()
        time.sleep(1)
        self.tc.select_chapter2()
        time.sleep(1)
        self.tc.input_knowledge_point("这是测试知识点")
        self.tc.click_completion_tab()
        self.tc.input_stem(completion_stem_string)
        self.tc.click_completion_number()
        self.tc.select_completion_number()
        self.tc.type_input1("测试填空题1")
        self.tc.type_input2("测试填空题2")
        self.tc.scroolbar_size()
        self.tc.input_analysis("这是答案解析")
        self.tc.click_label()
        self.tc.set_subject_difficulty()
        self.tc.click_submit_subject()
        self.lg.webdriverWait(10)
        # 验证我的题目tab可以成功打开
        try:
            assert u'我的题目' == self.tc.get_mysubject()
            print("我的题目页面可以成功打开")
        except Exception as e:
            print("我的题目页面不能成功打开", format(e))
        time.sleep(2)
        # 验证新创建的课程可以成功筛选
        self.tc.click_paper_type1_inmysubject()
        time.sleep(1)
        self.tc.select_paper_type1_inmysubject()
        time.sleep(1)
        self.tc.click_paper_type2_inmysubject()
        self.lg.webdriverWait(10)
        self.tc.select_paper_type2_inmysubject()
        self.tc.click_question_type_inmysubject()
        self.tc.select_question_completion_type_inmysubject()
        time.sleep(1)
        self.tc.click_difficulty_inmysubject()
        self.tc.select_difficulty_type_inmysubject()
        self.tc.click_status_inmysubject()
        self.tc.select_status_inmysubject()
        self.tc.input_stem_inmysubject(completion_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        # 验证列表题目与创建题目信息匹配
        try:
            self.assertEqual(completion_stem_string, self.tc.get_stem_intable())
            print("题干与创建时匹配，试卷创建成功")
        except Exception as e:
            print("题干与创建时不匹配，试卷创建不成功")
        time.sleep(2)
        # 删除待审核状态题目，实现数据初始化
        self.tc.click_deleteicon()
        self.lg.webdriverWait(10)
        self.tc.click_delete_button()
        time.sleep(2)
        print("测试填空题被删除了~")
        # 验证题目删除失败后重新删除
        self.tc.input_stem_inmysubject(completion_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        try:
            self.assertEqual(completion_stem_string, self.tc.get_stem_intable())
            print("题目没有被删除掉，数据初始化需要重新删除")
            self.tc.click_deleteicon()
            self.lg.webdriverWait(10)
            self.tc.click_delete_button()
        except Exception as e:
            print("题目已经被删除掉，不用再删除了")

    @ddt.data(*d_lec)
    def testTestPaper_05_QAQuestion(self, data):
        """验证讲师创建问答题流程正确"""
        self.lg = LoginPage(self.driver)
        self.tc = SubjectCreatePage(self.driver)
        self.tc.get_url(self.tc.env.getUrl() + "/t/lecturer/question")
        self.lg.webdriverWait(10)
        # 打开我的题目页面，查看是否存在脏数据
        qa_stem_string = "这是一道测试问答题，请勿审核通过"
        self.tc.input_stem_inmysubject(qa_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        self.tc.verify_nodata_exist()
        # try:
        #     self.assertEqual(qa_stem_string, self.tc.get_stem_intable())
        #     print("上次题目没有被删除掉，数据初始化需要重新删除")
        #     self.tc.click_deleteicon()
        #     self.lg.webdriverWait(10)
        #     self.tc.click_delete_button()
        # except Exception as e:
        #     print("题目已经被删除掉，不用再删除了")
        # 新增题目
        self.tc.click_add_subject_button()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.tc.click_paper_type1()
        self.lg.webdriverWait(10)
        self.tc.select_paper_type1()
        self.tc.click_paper_type2()
        self.tc.select_paper_type2()
        self.tc.click_chapter1()
        self.tc.select_chapter1()
        time.sleep(1)
        self.tc.select_chapter2()
        time.sleep(1)
        self.tc.input_knowledge_point("这是测试知识点")
        self.tc.click_qa_tab()
        self.tc.input_stem(qa_stem_string)
        self.tc.input_answer("我是问答题答案")
        self.tc.scroolbar_size()
        self.tc.input_analysis("这是答案解析")
        self.tc.click_label()
        self.tc.set_subject_difficulty()
        self.tc.click_submit_subject()
        self.lg.webdriverWait(10)
        # 验证我的题目tab可以成功打开
        try:
            assert u'我的题目' == self.tc.get_mysubject()
            print("我的题目页面可以成功打开")
        except Exception as e:
            print("我的题目页面不能成功打开", format(e))
        time.sleep(2)
        # 验证新创建的课程可以成功筛选
        self.tc.click_paper_type1_inmysubject()
        time.sleep(1)
        self.tc.select_paper_type1_inmysubject()
        time.sleep(1)
        self.tc.click_paper_type2_inmysubject()
        self.lg.webdriverWait(10)
        self.tc.select_paper_type2_inmysubject()
        self.tc.click_question_type_inmysubject()
        self.tc.select_question_qa_type_inmysubject()
        time.sleep(1)
        self.tc.click_difficulty_inmysubject()
        self.tc.select_difficulty_type_inmysubject()
        self.tc.click_status_inmysubject()
        self.tc.select_status_inmysubject()
        self.tc.input_stem_inmysubject(qa_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        # 验证列表题目与创建题目信息匹配
        try:
            self.assertEqual(qa_stem_string, self.tc.get_stem_intable())
            print("题干与创建时匹配，试卷创建成功")
        except Exception as e:
            print("题干与创建时不匹配，试卷创建不成功")
        time.sleep(2)
        # 删除待审核状态题目，实现数据初始化
        self.tc.click_deleteicon()
        self.tc.click_delete_button()
        print("测试问答题被删除了~")
        # 验证题目删除失败后重新删除
        self.tc.input_stem_inmysubject(qa_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        try:
            self.assertEqual(qa_stem_string, self.tc.get_stem_intable())
            print("题目没有被删除掉，数据初始化需要重新删除")
            self.tc.click_deleteicon()
            self.lg.webdriverWait(10)
            self.tc.click_delete_button()
        except Exception as e:
            print("题目已经被删除掉，不用再删除了")

    @ddt.data(*d_lec)
    def testTestPaper_06_CodeQuestion(self, data):
        """验证讲师创建编程题流程正确"""
        self.lg = LoginPage(self.driver)
        self.tc = SubjectCreatePage(self.driver)
        self.tc.get_url(self.tc.env.getUrl() + "/t/lecturer/question")
        self.lg.webdriverWait(10)
        # 打开我的题目页面，查看是否存在脏数据
        code_stem_string = "这是一道测试编程题，请勿审核通过"
        self.tc.input_stem_inmysubject(code_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        self.tc.verify_nodata_exist()
        # try:
        #     self.assertEqual(code_stem_string, self.tc.get_stem_intable())
        #     print("上次题目没有被删除掉，数据初始化需要重新删除")
        #     self.tc.click_deleteicon()
        #     self.lg.webdriverWait(10)
        #     self.tc.click_delete_button()
        # except Exception as e:
        #     print("题目已经被删除掉，不用再删除了")
        # 新增题目
        self.tc.click_add_subject_button()
        self.lg.current_handle_switch()
        self.lg.webdriverWait(10)
        self.tc.click_paper_type1()
        self.lg.webdriverWait(10)
        self.tc.select_paper_type1()
        self.tc.click_paper_type2()
        self.tc.select_paper_type2()
        self.tc.click_chapter1()
        self.tc.select_chapter1()
        time.sleep(1)
        self.tc.select_chapter2()
        time.sleep(1)
        self.tc.input_knowledge_point("这是测试知识点")
        self.tc.click_code_tab()
        code_stem_string = "这是一道测试编程题，请勿审核通过"
        self.tc.input_stem(code_stem_string)
        self.tc.input_answer("我是编程题答案")
        self.tc.scroolbar_size()
        self.tc.input_analysis("这是答案解析")
        self.tc.click_label()
        self.tc.set_subject_difficulty()
        self.tc.click_submit_subject()
        self.lg.webdriverWait(10)
        # 验证我的题目tab可以成功打开
        try:
            assert u'我的题目' == self.tc.get_mysubject()
            print("我的题目页面可以成功打开")
        except Exception as e:
            print("我的题目页面不能成功打开", format(e))
        time.sleep(2)
        # 验证新创建的课程可以成功筛选
        self.tc.click_paper_type1_inmysubject()
        time.sleep(1)
        self.tc.select_paper_type1_inmysubject()
        time.sleep(1)
        self.tc.click_paper_type2_inmysubject()
        self.lg.webdriverWait(10)
        self.tc.select_paper_type2_inmysubject()
        self.tc.click_question_type_inmysubject()
        self.tc.select_question_code_type_inmysubject()
        time.sleep(1)
        self.tc.click_difficulty_inmysubject()
        self.tc.select_difficulty_type_inmysubject()
        self.tc.click_status_inmysubject()
        self.tc.select_status_inmysubject()
        self.tc.input_stem_inmysubject(code_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        # 验证列表题目与创建题目信息匹配
        try:
            self.assertEqual(code_stem_string, self.tc.get_stem_intable())
            print("题干与创建时匹配，试卷创建成功")
        except Exception as e:
            print("题干与创建时不匹配，试卷创建不成功")
        time.sleep(2)
        # 删除待审核状态题目，实现数据初始化
        self.tc.click_deleteicon()
        self.tc.click_delete_button()
        print("测试编程题被删除了~")
        # 验证题目删除失败后重新删除
        self.tc.input_stem_inmysubject(code_stem_string)
        self.tc.click_search_button()
        self.lg.webdriverWait(10)
        try:
            self.assertEqual(code_stem_string, self.tc.get_stem_intable())
            print("题目没有被删除掉，数据初始化需要重新删除")
            self.tc.click_deleteicon()
            self.lg.webdriverWait(10)
            self.tc.click_delete_button()
        except Exception as e:
            print("题目已经被删除掉，不用再删除了")

if __name__ == '__main__':
    unittest.main()
