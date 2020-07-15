#coding=utf-8
from Pages.BasePage import BasePage

class FavoritesPage(BasePage):
    #旧版本course_favorite_icon = "xpath>//span[@id='fav']/i"
    course_favorite_icon="xpath>//span[@id='fav']/i"
    course_favorite_num="xpath>//*[@id='favNum']"
    #旧版本 course_title="xpath>//*[@id='CourseTitle']"
    course_title="xpath>//span[@class='til']"
    login_link="xpath>//div[2]/div/ul/li[9]/a"
    account_login="xpath>//*[@id='login-wechat']/div[1]/div/a"
    user_name="xpath>//*[@id='loginform-username']"
    password="xpath>//*[@id='loginform-password']"
    login_button="xpath>//input[@name='login-button']"
    study_center="xpath>//a[contains(text(),'学习中心')]"
    favorite_tab="xpath>//div[@class='userTabs']/div[@class='Page']/ul/li[5]/a"
    my_fav_course="xpath>//*[@id='PubList']/li[1]/div[2]/h2/a"
    weixin_pop="xpath>//div[@class='qrcode-con']"
    nexttime_say="xpath>//div[@class='btn-close']"

    def get_coursetitle_text(self):
        return self.get_element(self.course_title).text

    def click_fav_course_icon(self):
        self.click(self.course_favorite_icon)


    def get_fav_course_number(self):
        return self.get_element(self.course_favorite_num).text

    def click_LoginLink(self):
        self.click(self.login_link)

    def click_AccountLogin(self):
        self.click(self.account_login)

    def get_AccountLogin_text(self):
        print(self.get_element(self.account_login).text)
        return self.get_element(self.account_login).text

    def type_UserName(self, text):
        self.type(self.user_name, text)

    def type_password(self, text):
        self.type(self.password, text)

    def click_LoginButton(self):
        self.click(self.login_button)

    def click_StudyCenter(self):
        self.click(self.study_center)

    def click_myfav(self):
        self.click(self.favorite_tab)

    def get_favcoursetitle_text(self):
        return self.get_element(self.my_fav_course).text

    #关闭关注微信弹框
    def close_weixin_pop(self):
        flag=self.isElementExist(self.weixin_pop)
        if flag:
            print("微信关注弹框出现，需要关闭哦")
            self.click(self.nexttime_say)
        else:
            print("微信弹框没有出现，不需要关闭哦")
