#coding=utf-8
from Pages.BasePage import BasePage
import time
import os
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

class LoginPage(BasePage):
    img_close = "xpath>//span[@class='offbtn offbtn-center']"
    login_link = "xpath>//a[contains(@class,'other LoginReg')] "
    account_login = "xpath>//div[@id='login-wechat']/div[3]/a"

    #关闭活动弹窗
    def close_active_pop(self):
        flag = self.isElementExist(self.img_close)
        if flag:
            print("弹框出现，需要关闭喽")
            self.click(self.img_close)
        else:
            print("没有活动弹窗")

    #关闭关注弹框
    def close_focus_pop(self):
        flag=self.isElementExist(self.focus_next)
        if flag:
            print("关注弹框出现，需要关闭哦")
            self.click(self.focus_next)
        else:
            print("关注弹框没有弹出，不需要关闭")

    #关闭讲师中心通知弹框
    def close_teach_notice_pop(self):
        flag=self.isElementExist(self.teach_notice_pop)
        if flag:
            print("讲师中心有新功能上线通知弹框")
            self.click(self.teach_notice_pop)
        else:
            print("没有讲师新功能上线通知弹框")

    def get_StudyCenter_text(self):
        return self.get_element(self.study_center).text

    def click_Close(self):
        self.click(self.img_close)

    def click_LoginLink(self):
        self.click(self.login_link)


        return self.get_element(self.passerror).text

    def get_error_info(self,info):
        try:
            if info=='1':
                text=self.get_usernull_message()
            else:
                text=self.get_accouterror_message()
            return text
        except Exception as e:
            print("登录异常")

    def Halt_exit(self):
        move_to_element = self.get_element(self.user_info)
        ActionChains(self.driver).move_to_element(move_to_element).perform()
        self.click(self.login_out)

    def Login_Account(self,username,password):
        self.close_active_pop()
        self.click_LoginLink()
        self.click_AccountLogin()
        sleep(2)
        self.send_UserName(username)
        self.send_password(password)
        self.click_LoginButton()
        sleep(2)
