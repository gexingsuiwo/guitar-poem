#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from http import cookiejar
from urllib import parse
from urllib import request
from bs4 import BeautifulSoup
import re
#导入re模块
import re
import os
import sys

class Spider:
    def __init__(self):
        # User-Agent信息
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        # Headers信息
        self.head = {'User-Agent': user_agent, 'Connection': 'keep-alive'}

        pass
    #
    def mkdir(self, path):
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
            return True
        else:
            return False

    def mkdir(self, path):
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
            return True
        else:
            return False

    def get_pic(self, url, title):

        req = request.Request(url=url, headers=self.head)
        reponse = request.urlopen(req)
        data = reponse.read().decode('gbk')

        soup = BeautifulSoup(data, "html.parser")
        e = soup.select('.device img')
        print(e)
        if len(e) > 0:
            #创建目录
            path = sys.path[0] + '/吉他曲谱/' + self.keyword + '/' + title
            self.mkdir(path)

            self.head['Referer'] = url
            #抓取图片
            print("正在为你下载曲谱《%s》..." % title)

            for item in e:

                imgurl = 'http://www.ccguitar.cn/' + item.get('src')
                alt = item.get('alt')

                print(imgurl)

                req1 = request.Request(imgurl, headers=self.head)
                reponse = request.urlopen(req1)
                data = reponse.read()

                filename = "{}/{}".format(path, os.path.basename(imgurl))

                with open(filename, 'wb') as f:
                    f.write(data)

        else:
            print("很抱歉，没有曲谱哦~")

    def getPage(self):
        self.keyword = input('请输入歌曲名：')
        keyword = parse.quote(self.keyword.encode('gbk'))
        url = "http://so.ccguitar.cn/tosearch.aspx?searchname=%s&pu_gs=3&seachtype=1" % keyword

        #创建Request对象
        req = request.Request(url=url, headers=self.head)
        response = request.urlopen(req)

        content = response.read().decode('gbk')
        soup = BeautifulSoup(content, "html.parser")
        s = soup.select('.search_url a')
        if len(s) > 0:
            for index,item in enumerate(s):
                title = item.get_text().strip().rstrip('.')
                url = item.get('href')

                self.get_pic(url, title)
        else:
            print("很抱歉，没有相关曲谱哦~")
            self.getPage()

spider = Spider()
spider.getPage()





