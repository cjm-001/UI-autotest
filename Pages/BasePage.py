#coding=utf-8
import os.path
from selenium.webdriver.support.ui import WebDriverWait
from common.logger import Logger
import time
import configparser
from env.EnvFactory import EnvFactory

logger=Logger(logger="BasePage").getlog()

class BasePage(object):
    def __init__(self,driver):
        self.driver = driver
        config = configparser.ConfigParser()
        file_path = os.path.dirname(os.path.abspath('.')) + '/config/config.ini'
        config.read(file_path)
        envname = config.get("testServer", "env")
        ef = EnvFactory()
        env = ef.getEnv(envname)
        self.env = env
        self.config = config

    def quit_browser(self):
        self.driver.quit()

    def refresh(self):
        self.driver.refresh()

    def forward(self):
        self.driver.forward()
        logger.info("click forward on current page")

    def back(self):
        self.driver.back()
        logger.info("click back on current page")

    def delete_cookie(self):
        self.driver.delete_all_cookies()
        logger.info("Delete cookies successfully")

    def get_url(self,URL):
        self.driver.get(URL)
        logger.info("go to new url succefully")

    def close_window(self):
        try:
            self.driver.close()
            logger.info("closing and quit browser")
        except:
            logger.info("failed to quit the browser")

    def get_page_title(self):
        logger.info("current page title is %s" % self.driver.title)
        return self.driver.title

    # 保存图片
    def get_windows_img(self):
        file_path = os.path.dirname(os.path.abspath('.')) + '/screenshot/'
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        screen_name = file_path + rq + '.png'
        try:
            self.driver.get_screenshot_as_file(screen_name)
            logger.info("Had take screenshot and save to folder : /screenshots")
        except NameError as e:
            logger.error("Failed to take screenshot! %s" % e)
            self.get_windows_img()

    # 输入
    def type(self,selector,text):

        el = self.get_element(selector)
        el.clear()
        try:
            el.send_keys(text)
            logger.info("Had type \' %s \' in inputBox" % text)
        except NameError as e:
            logger.error("Failed to type in input box with %s" % e)
            self.get_windows_img()

    # 清除文本框
    def clear(self,selector):

        el = self.get_element(selector)
        try:
            el.clear()
            logger.info("Clear text in input box before typing.")
        except NameError as e:
            logger.error("Failed to clear in input box with %s" % e)
            self.get_windows_img()

    # 点击元素
    def click(self,selector):
        el = self.get_element(selector)
        try:
            el.click()
        except NameError as e:
            logger.error("Failed to click the element with %s" % e)

    # 点击元素_new
    def click_new(self,selector):
        el = self.get_element1(selector)
        try:
            el.click()
        except NameError as e:
            logger.error("Failed to click the element with %s" % e)


    #定义script方法，用于执行js脚本
    def script(self,src):
        self.driver.execute_script(src)

    #定义script方法，执行js脚本，移动元素至指定位置
    def script_target(self,src):
        self.driver.execute_script("arguments[0].scrollIntoView();",src)

    #定义switch_frame方法，用于页面切换
    def switch_frame(self,loc):
        return self.driver.switch_to_frame(loc)

    #   该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false
    def isElementExist(self,element):
        flag = False
        try:
            return self.get_element(element)
        except:
            return flag
    def get_element1(self, selector,timeout=10):
        if '>' not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split('>')[0]
        selector_value = selector.split('>')[1]

        if selector_by == "i" or selector_by == 'id':
            element = self.driver.find_element_by_id(selector_value)
        elif selector_by == "n" or selector_by == 'name':
            element = self.driver.find_element_by_name(selector_value)
        elif selector_by == "c" or selector_by == 'class_name':
            element = self.driver.find_element_by_class_name(selector_value)
        elif selector_by == "l" or selector_by == 'link_text':
            element = self.driver.find_element_by_link_text(selector_value)
        elif selector_by == "p" or selector_by == 'partial_link_text':
            element = self.driver.find_element_by_partial_link_text(selector_value)
        elif selector_by == "t" or selector_by == 'tag_name':
            element = self.driver.find_element_by_tag_name(selector_value)
        elif selector_by == "x" or selector_by == 'xpath':
            #ui.WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.XPATH, selector_value)))
            element = self.driver.find_element_by_xpath(selector_value)
        elif selector_by == "s" or selector_by == 'selector_selector':
            element = self.driver.find_element_by_css_selector(selector_value)
        else:
            raise NameError("Please enter a valid type of targeting elements.")

        return element

    def get_element(self,key):
        try:
            if '>' not in key:
                return self.driver.find_element_by_id(key)
            by=key.split('>')[0]
            value=key.split('>')[1]
            if by=='id':
                element=self.driver.find_element_by_id(value)
            elif by=='name':
                element =self.driver.find_element_by_name(value)
            elif by=='className':
                element =self.driver.find_element_by_class_name(value)
            elif by=='css':
                element =self.driver.find_element_by_css_selector(value)
            else:
                element =self.driver.find_element_by_xpath(value)
            WebDriverWait(self.driver,10).until(lambda driver:element.is_displayed())
            return element
        except:
            print("元素没有出现，等待超时")

    # 封装隐式等待
    def webdriverWait(self,seconds):
        self.driver.implicitly_wait(seconds)
        logger.info("wait for %s" %seconds)

    #封装页面切换,关闭之前页面
    def current_handle_switch(self):
        all_handles=self.driver.window_handles
        for handle in all_handles:
            if handle!=self.driver.current_window_handle:
                print("switch to next window")
                logger.info("switch to next window")
                self.driver.close()
                self.driver.switch_to.window(handle)

    #封装页面切换到最新打开页面，不关闭之前页面
    def switch_window_without_close(self):
        windows=self.driver.window_handles
        self.driver.switch_to.window(windows[-1])

    #封装页面切换到之前打开页面，不关闭之前页面
    def switch_previous_window(self):
        windows=self.driver.window_handles
        self.driver.switch_to.window(windows[0])

    #切换为至第一个窗口
    def switch_One_window(self):
        all_h = self.driver.window_handles
        print(all_h)
        self.driver.switch_to.window(all_h[0])

        # 切换当前窗口

    def switch_window(self):
        handles = self.driver.window_handles
        print(handles)
        for handle in handles:
            if handle != self.driver.current_window_handle:
                print("swich to second window", handle)
                self.driver.switch_to.window(handle)

    #退出iframe窗口
    def signout_frame(self):
        self.driver.switch_to.default_content()



