#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,os
import time
import requests
from bs4 import BeautifulSoup
import readability

page_url = 'http://coolshell.cn/page/'
max_page = 68 

UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/44.0.2403.155 Safari/537.36"
headers = {
            "User-Agent": "UA",
            "Host": "coolshell.cn",
        }

s = requests.Session()

def make_soup(url, tag, name):
    page = get_page(url)
    soup = BeautifulSoup(page)
    what_we_got = soup.find_all(attrs={tag:name})
    return what_we_got

def get_page(url):
    page = s.get(url, headers=headers, verify=False).text
    return page

def save_file(filename, content):
    filepath = os.path.dirname(filename)
    if (False == os.path.exists(filepath)):
        os.makedirs(filepath)
    if (os.path.exists(filename)):
        print filename, " already exists!"
        return
    f = open(filename, "w+")
    f.write(content)
    f.close

def get_html(url):
    print url
    page = s.get(url, headers=headers, verify=False).text
    page = page.encode("utf-8")
    html = readability.Readability(page, url)
    filename =  "./coolshell/" + html.getArticleTitle().encode("utf-8") + ".html"
    print filename
    #filename = filename.decode("utf-8").encode("gbk","ignore")
    content = html.grabArticle().encode("utf-8")
    content = content.decode("utf-8").encode("gbk","ignore")
    save_file(filename, content)

def get_article_url(page_url):
    for index in range(max_page):
        url = page_url + str(index)
        tag_li = make_soup(url, "class", "title")
        print index
        print url
        time.sleep(6)
        for tag in tag_li:
            #print type(tag)
            try:
                #print tag.renderContents()
                article_url =  tag['href']
            except KeyError:
                continue
            get_html(article_url)            
            
if __name__ == '__main__':            
    get_article_url(page_url)
