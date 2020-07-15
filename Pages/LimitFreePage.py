#coding=utf-8
from Pages.BasePage import BasePage
from selenium.webdriver.common.action_chains import ActionChains
import time

class LimitFreePage(BasePage):
    limit_free_tab="xpath>//a[@id='navLimitFree']"
    new_course_free="xpath>//div[@id='newcourse']//span"
    first_free="xpath>//div[@id='newcourse']//div[3]//div[@class='si_vip']"
    first_course_pic="xpath>//div[@id='newcourse']//div[3]//img"
    limit_free_button_old="xpath>//div[@id='buyBtns']/button[3]"
    limit_free_button_new="xpath>//div[@class='goVipSign']"
    course_list_old="xpath>//dt[@id='tabsTil']/p[2]"
    course_list_new="xpath>//ul[@class='tabs-list clearfix2']/li[2]"
    first_free_course="xpath>//ul[@id='syList']/li[1]/div"
    start_look="xpath>//ul[@id='syList']/li[1]//a/span"
    check_vip_free_old="xpath>//div[@class='Top']/a[2]"
    check_vip_free_new="xpath>//a[text()='会员限时免费']"
    chap_icon = "xpath>//ul[@id='syList']//i[@class='icon']"
    first_free_second_row = "xpath>//ul[@id='syList']/li[2]/div"
    start_look_second_row = "xpath>//ul[@id='syList']/li[2]//a/span"


    def click_limit_free(self):
        self.click(self.limit_free_tab)

    def get_new_course_free(self):
        return self.get_element(self.new_course_free).text

    def first_free_label(self):
        return self.get_element(self.first_free).text

    def click_first_pic(self):
        self.click(self.first_course_pic)

    def verify_limit_free_button(self):
        flag=self.isElementExist(self.limit_free_button_new)
        flag2 = self.isElementExist(self.limit_free_button_old)
        if flag:
            print("新版会员限免按钮存在，会员可以限时免费观看")
        elif flag2:
            print("旧版会员限免按钮存在，会员可以限时免费观看")
        else:
            print("会员限免按钮不存在，会员无法限时免费观看")

    def click_course_list(self):
        flag_old=self.isElementExist(self.course_list_old)
        flag_new=self.isElementExist(self.course_list_new)
        if flag_old:
            print("旧版课程大纲元素存在，点击切换")
            self.click(self.course_list_old)
        elif flag_new:
            print("新版课程大纲存在，需要点击切换")
            self.click(self.course_list_new)
        else:
            print("新旧版本课程大纲元素都没有出现，无法点击哦")

    def verify_chap_icon(self):
        flag=self.isElementExist(self.chap_icon)
        if flag:
            self.look_first_lesson_second_row()
            print("课程分章节显示，需要点击第二行课时才能播放")
        else:
            self.look_first_lesson_first_row()
            print("课程没有章信息，直接点击第一行课时就可以播放")

    def look_first_lesson_first_row(self):
        move_to_elment=self.get_element(self.first_free_course)
        ActionChains(self.driver).move_to_element(move_to_elment).perform()
        self.click(self.start_look)
        time.sleep(2)

    def look_first_lesson_second_row(self):
        mov_to_elment=self.get_element(self.first_free_second_row)
        ActionChains(self.driver).move_to_element(mov_to_elment).perform()
        self.click(self.start_look_second_row)
        time.sleep(2)

    def get_vip_free_button(self):
        flag_old=self.get_element(self.check_vip_free_old)
        flag_new=self.get_element(self.check_vip_free_new)
        if flag_old:
            print("旧版会员限时免费按钮存在")
        elif flag_new:
            print("新版会员限免按钮存在")
        else:
            print("会员限时免费按钮不存在，需要检查原因")
