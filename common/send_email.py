#coding=utf-8
import time
import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from common.logger import Logger

mylogger=Logger(logger='send_email').getlog()

# ======查找测试目录，找到最新生成的测试报告文件======
def new_report(test_report):
    lists = os.listdir(test_report)  # 列出目录的下所有文件和文件夹保存到lists
    lists.sort(key=lambda fn: os.path.getmtime(test_report + '\\' + fn))  # 按时间排序
    file_new = os.path.join(test_report, lists[-1])  # 获取最新的文件保存到file_new
    print(file_new)
    return file_new

def send_mail(new_report,new_report_file,now):
    senduser='' #发件人邮箱
    sendpswd=''  #发件人邮箱密码
    receuser1 = ''  # 收件人1邮箱

    #获取报告文件
    f=open(new_report,'rb')
    mail_body=f.read()
    f.close()

    msg=MIMEMultipart()
    #邮件内容
    text=MIMEText(mail_body,'html','utf-8')
    msg.attach(text)

    #邮件标题
    msg['Subject']=Header('自动化测试报告','utf-8')
    msg['From']=senduser
    msg['To']=receuser1;receuser2

    #发送附件
    att = MIMEApplication(open(new_report_file, 'rb').read())
    att['Content-Type']='application/octet-stream'
    att.add_header("Content-Disposition","attachement",filename=("utf-8","",now+"_report.html"))
    msg.attach(att)

    server=smtplib.SMTP_SSL("smtp.qq.com",465)
    mylogger.info('连接QQ邮箱smtp服务')
    server.login(senduser,sendpswd)
    mylogger.info("连接成功")
    server.sendmail(senduser,[receuser1,receuser2],msg.as_string())
    #server.sendmail(senduser, [receuser2], msg.as_string())
    server.quit()
    mylogger.info("邮件发送成功")


