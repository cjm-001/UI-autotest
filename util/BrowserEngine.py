# coding=utf-8
import configparser
import os.path
from env.EnvFactory import EnvFactory
from selenium import webdriver
from common.logger import Logger

logger = Logger(logger="BrowserEngine").getlog()

class BrowserEngine(object):

    dir = os.path.dirname(os.path.abspath('.'))
    Chrome_driver_path = dir + '/drivers/chromedriver.exe'
    firefox_driver_path = dir + '/drivers/geckodriver.exe'
    def __init__(self,driver):
        self.driver = driver

    def open_browser(self,driver):
        config = configparser.ConfigParser()
        file_path = os.path.dirname(os.path.abspath('.')) + '/config/config.ini'
        config.read(file_path)

        browser = config.get("browserType","browserName")
        logger.info("You had select %s browser." %browser)
        envname = config.get("testServer","env")

        ef = EnvFactory()
        env = ef.getEnv(envname)
        self.env = env
        url = env.getUrl()
        logger.info("The test server url is: %s" % url)

        if browser == "Firefox":
            driver = webdriver.Firefox(self.firefox_driver_path)
            logger.info("打开火狐浏览器")
        else:
            driver = webdriver.Chrome(self.Chrome_driver_path)
            logger.info("打开谷歌浏览器")

        driver.get(url)
        logger.info("open url: %s" % url)
        #driver.set_window_size(1936, 1056)
        driver.maximize_window()
        logger.info("最大化窗口")
        driver.get_window_size()
        logger.info("获取窗口大小")
        print(driver.get_window_size())
        driver.get_window_position()
        logger.info("获取窗口位置")
        print(driver.get_window_position())
        driver.implicitly_wait(3)
        logger.info("等待3s")
        return driver
    def quit_driver(self):
        logger.info("Now, Close and quit the browser.")
        self.driver.quit()