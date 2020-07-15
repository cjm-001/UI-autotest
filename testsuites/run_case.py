#coding=utf-8
import unittest
import os
import HTMLTestRunner
import time
from common import send_email
from common import send_dingnotice

#测试用例路径
case_path=os.path.join(os.path.dirname(os.path.abspath('.'))+'\Cases')
#测试报告路径
report_dir=os.path.join(os.path.dirname(os.path.abspath('.'))+r'\report')

def RunAllCase():
    testcase=unittest.TestSuite()
    discover=unittest.defaultTestLoader.discover(case_path,pattern='*Case.py',top_level_dir=None)

    for test_suite in discover:
        for test_case in test_suite:
            print(test_case)
            testcase.addTest(test_case)
    return testcase

if __name__=='__main__':
    #获取生成报告的时间
    now=time.strftime("%Y-%m-%d_%H-%M-%S")
    #创建完整报告文件
    filename=report_dir+'\\'+now+'_result.html'
    fp=open(filename,'wb')

    runner=HTMLTestRunner.HTMLTestRunner(stream=fp,title=u"核心业务自动化测试报告",description=u"用例执行结果如下:")
    re=runner.run(RunAllCase())
    fp.close()

    #查找最新生成的报告
    new_report=send_email.new_report(report_dir)

    #发送钉钉消息
    message=send_dingnotice.send_message_to_robot(re.success_count,  re.failure_count, re.error_count)

    #发送邮件
    send_email.send_mail(new_report, filename, now)
