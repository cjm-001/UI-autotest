#coding=utf-8
import configparser
import os
class ReadIni(object):
    dir=os.path.dirname(os.path.abspath('.'))
    print(dir)
    def __init__(self,file_name=None,node=None):
        if file_name==None:
            file_name=os.path.dirname(os.path.abspath('.'))+'/config/LocalElement.ini'
        if node==None:
            self.node="LoginElement"
        else:
            self.node=node
        self.cf=self.load_ini(file_name)

    #加载文件
    def load_ini(self,file_name):
        cf=configparser.ConfigParser()
        cf.read(file_name)
        return cf

    #获取value值
    def get_value(self,key):
        data=self.cf.get(self.node,key)
        return data


    #读取浏览器信息
    def get_browser_value(self):
        root_dir=os.path.dirname(os.path.abspath('.')) #获得项目的绝对路径
        print(root_dir)

        config=configparser.ConfigParser()
        file_path=os.path.dirname(os.path.abspath('.'))+'/config/config.ini'
        config.read(file_path)

        browser=config.get("browserType","browserName")
        url=config.get("testServer","URL")

        return(browser,url)


