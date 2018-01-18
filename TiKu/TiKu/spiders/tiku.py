#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@TIME   :2018/1/15 16:21
import scrapy,requests,re,time
from bs4 import BeautifulSoup
from scrapy.spiders import  Request
from ..items import TikuItem

from scrapy.spiders import CrawlSpider,Rule ##CrawlSpider与Rule配合使用可以骑到历遍全站的作用
from scrapy.linkextractors import LinkExtractor
from scrapy import FormRequest  ##Scrapy中用作登录使用的一个包
userName='1090211957@qq.com'
userPassword='66d2b83106e7d4d4cbd0a16600f3d16e'

class MySpider(scrapy.Spider):
    name='tiku'
    allowed_domains = ['exam.bdqn.cn']
    bash_url = 'http://exam.bdqn.cn/testing/'
    bashurl = '.html'
    start_urls=['http://exam.bdqn.cn/testing/login','http://exam.bdqn.cn:80/testing/login']

    cookies = {
        'examLoginUserName': '1090211957@qq.com',
        'JSESSIONID': '3E971207126E24D0F60B129CF619993B.exam-tomcat-node3.exam-tomcat-node3'
    }
    headers = {
        # 'Connection': 'keep - alive',  # 保持链接状态
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
    }
    #登录
    def start_requests(self):

        # meta = {
        #     'dont_redirect': True,  # 禁止网页重定向
        #     'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
        # }
        yield Request(url=self.start_urls[1],headers=self.headers,cookies=self.cookies,callback=self.login_ok,meta={'cookiejar':1},method='POST')

    def login_ok(self,response):
        print('login_ok当前网页地址:', response.url)
        if (response.url)[:39]=='http://exam.bdqn.cn/testing/index/49211':
            print('登陆成功')
            tra=BeautifulSoup(response.text,'lxml').find('a',title='我的历史')
            url=tra['href']
            print('获得我的历史地址:',url)
            #url = self.bash_url + 'hisory'
            # http://exam.bdqn.cn/testing/history
            yield Request(url=url,callback=self.go_history,meta={'cookiejar': response.meta['cookiejar']})
        else:
            print('登录失败')
            return

    #跳转到我的历史界面
    #不要使用parse函数、因为CrawlSpider使用的parse来实现逻辑、如果你使用了parse函数、CrawlSpider会运行失败。
    def go_history(self, response):
        print('go_history当前网页地址:',response.url)
        #http://exam.bdqn.cn:80/testing/history
        page_num = 2
        # 获取前6页内容
        for i in range(1,int(page_num)+1):
            #http://exam.bdqn.cn/testing/history?page=2
            #http://exam.bdqn.cn/testing/history/classExam?page=2
            url=response.url+'?page='+str(i)
            time.sleep(1)
            yield Request(url=url,callback=self.find_list,meta={'cookiejar': response.meta['cookiejar']})

    #在每页中找到试题分析的链接
    def find_list(self,response):
        print('find_list当前网页地址:', response.url)
        urls=re.findall(r'<a href="(.*?)" title="" class="sec3">试 题 分 析</a>',response.text)
        #urls = re.findall(r'<td class="L"><a href="(.*?)">(.*?)</a></td>', response.text)
        # 获得所有试题分析网址列表 'paper/solutions/23623892/45961278'
        for url in urls:
            #http://exam.bdqn.cn/testing/paper/solutions/23623073/45958656
            url=self.bash_url+str(url)
            time.sleep(1)
            yield Request(url=url,callback=self.down_answer,meta={'cookiejar': response.meta['cookiejar']})


    #获取当前页面所有题答案
    def down_answer(self,response):
        tras=BeautifulSoup(response.text, 'lxml').find_all('div',class_='sec2 grays')
        ids=[]
        if len(ids)==0:
            for tra in tras:
                id=tra.find('image')['src']  #http://exam.bdqn.cn:80/testing/cdn/getImage?relativePath=0002000/0001303/1303_1460855618159.png
                ids.append(id)
        else:
            ids=[]
            for tra in tras:
                id = tra.find('image')[
                    'src']  # http://exam.bdqn.cn:80/testing/cdn/getImage?relativePath=0002000/0001303/1303_1460855618159.png
                ids.append(id)
        #问题
        answer = re.findall(r'正确答案是<em>(.*?)</em>',response.text)
        #答案
        for i,o in zip(ids,answer):
            text=i.split('/')
            # print((i['src'])[-22:]) 1339_1460855640050.png
            id=text[7]
            # print((i['src'])[-38:-31]) 0002000
            sort_id=text[6]
            answer=o
            item = TikuItem()
            item['id'] = id
            item['sort_id'] = sort_id
            item['answer'] = answer
            yield item


