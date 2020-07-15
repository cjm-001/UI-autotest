#coding=utf-8
from Pages.BasePage import BasePage
from selenium.webdriver.common.action_chains import ActionChains
import time

class FreeCoursePage(BasePage):
    free_tab="xpath>//a[@id='navFree']"
    free_checked="xpath>//div[@id='listContent']//a[3]/i"
    first_free_text="xpath>//div[@class='cList']//div[1]//div[3]//h4"
    first_image="xpath>//div[@class='cList']/div[1]//img"
    free_label="xpath>//span[@class='new']/b"
    course_list="xpath>//section[@class='main-content-wrap']/ul/li[last()-3]"
    chap_icon_new="xpath>//ul[@id='syList']/li[1]/div/i[1]"
    first_free_course="xpath>//ul[@id='syList']/li[1]/div/span"
    start_look="xpath>//ul[@id='syList']/li[1]/div/a[2]/span"
    first_free_second_row="xpath>//ul[@id='syList']/li[2]/div/span"
    start_look_second_row="xpath>//ul[@id='syList']/li[2]/div/a[2]/span"
    current_play="xpath>//div[2]/div[@class='VideoTop clearfix2']/span"


    def click_free_tab(self):
        self.click(self.free_tab)

    def verify_free_checked(self):
        flag = self.isElementExist(self.free_checked)
        if flag:
            print("免费课程复选框被选中，页面跳转正确")
        else:
            print("免费课程复选框没有被选中，页面跳转不正确")

    def verify_first_free_text(self):
        flag=self.isElementExist(self.first_free_text)
        if flag:
            print("第一个课程为免费课程，课程列表数据展示正常")
        else:
            print("第一个课程不是免费课程，课程列表数据展示不正常")

    def click_first_image(self):
        self.click(self.first_image)

    def get_free_label(self):
        return self.get_element(self.free_label).text

    def click_course_list(self):
        self.click(self.course_list)

    def verify_chap_icon(self):
        flag=self.isElementExist(self.chap_icon_new)
        if flag:
            self.look_first_lesson_second_row()
            print("课程分章节显示，需要点击第二行课时才能播放")
        else:
            self.look_first_lesson_first_row()
            print("课程没有章信息，直接点击第一行课时就可以播放")



    def look_first_lesson_first_row(self):
        mov_to_element=self.get_element(self.first_free_course)
        ActionChains(self.driver).move_to_element(mov_to_element).perform()
        self.click(self.start_look)
        time.sleep(2)

    def look_first_lesson_second_row(self):
        mov_to_element=self.get_element(self.first_free_second_row)
        ActionChains(self.driver).move_to_element(mov_to_element).perform()
        self.click(self.start_look_second_row)
        time.sleep(2)

    def get_current_play(self):
        return self.get_element(self.current_play).text



