#coding=utf-8
from Pages.BasePage import BasePage
from selenium.webdriver.common.action_chains import ActionChains
import time

class WejobStudyCenterPage(BasePage):
    webmap="xpath>//span[@class='tab_list']"
    wejob_enter="xpath>//div[@class='tab_more network_list']/ul[1]/li[2]/a"
    wejob_link = "xpath>//a[@id='navWejob']"
    study_center="xpath>//ul[@id='wjw_nav']/ul/li[1]/a"
    course_number="xpath>//div[@class='study']/p"
    course_tab="xpath>//div[@class='study-tab']/a[2]"
    no_buy="xpath>//div[@class='lesson']/p"
    go_button="xpath>//div[@class='lesson']/a"
    ok_button="xpath>//div[@class='mask-content']//button"


    def wejob_enter_method(self):
        move_to_element = self.get_element(self.webmap)
        ActionChains(self.driver).move_to_element(move_to_element).perform()
        self.click(self.wejob_enter)
        time.sleep(2)

    def click_study_center(self):
        self.click(self.study_center)

    def get_class_number(self):
        return self.get_element(self.course_number).text

    def click_course_tab(self):
        self.click(self.course_tab)

    def get_notbuy_text(self):
        return self.get_element(self.no_buy).text

    def click_gobutton(self):
        self.click(self.go_button)

    def verify_ok_exist(self):
        flag=self.isElementExist(self.ok_button)
        if flag:
            print("提示浮层出现，需要点击哦")
            self.click(self.ok_button)
        else:
            print("提示浮层没有出现，不需要操作")

