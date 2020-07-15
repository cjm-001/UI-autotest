#coding=utf-8
from Pages.BasePage import BasePage

class NewsPage(BasePage):
    js_bottom="window.scrollTo(0,document.body.scrollHeight)" # 滑动滚动条到底部
    news_more="xpath>//*[@id='nav_newsList']/div/a"
    news_center="xpath>//div[@class='Content Message']/div/div/ul/li"
    first_news="xpath>//div[@class='Content Message']/div/div[2]/dl[1]/dt/a"
    news_title="xpath>//div[@class='Page']/dl/h4"

    # 滚动滚动条到底部
    def scroolbar_bottom(self):
        self.script(self.js_bottom)

    def click_newsmore(self):
        self.click(self.news_more)

    def get_newscenter_text(self):
        return self.get_element(self.news_center).text

    def click_firstnews(self):
        self.click(self.first_news)

    def get_newstitle_fromlist(self):
        return self.get_element(self.first_news).text

    def get_newtitle_fromdetail(self):
        return self.get_element(self.news_title).text

