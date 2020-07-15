#coding=utf-8
import requests
from common.logger import Logger

mylogger=Logger(logger='send_dingnotice').getlog()

HEADERS={'ua':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'}
DINGDING_URL=''

def send_message_to_robot(passed, failed,error):
    url=DINGDING_URL
    message= "test"
    message={"msgtype":"text","text":{"content":message,"title":"UI自动化结果通知"}}
    try:
        resp=requests.post(url,headers=HEADERS,json=message,timeout=(3,60))
    except:
        print("Send Message is fail!");


