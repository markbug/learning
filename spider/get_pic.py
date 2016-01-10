#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,os
import time
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')
page_url = 'http://www.douban.com/group/haixiuzu/discussion?start='
max_page = 3000

pic_info_file = "pic_info.txt"

UA = ["Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"]

header_li = [{
            "User-Agent": "UA[0]",
            "Host": "www.douban.com",
        },
        {
            "User-Agent": "UA[1]",
            "Host": "www.douban.com",
        },
        {
            "User-Agent": "UA[2]",
            "Host": "www.douban.com",
        },
        {
            "User-Agent": "UA[3]",
            "Host": "www.douban.com",
        },
        {
            "User-Agent": "UA[4]",
            "Host": "www.douban.com",
        }
        ]
header_num = 0

s = requests.Session()

def save_pic_info(item):
    f =open(pic_info_file, "a+")
    f.write("".join(str(item)) + os.linesep)
    f.close

def save_pic(pic_url):
    file_name = pic_url.split("/")[-1]
    #print file_name
    real_pic_r = s.get(pic_url, headers=header_li[header_num], stream=True)
    path = os.getcwd()
    path = os.path.join(path, 'pictures')
    if not os.path.exists(path):
        os.mkdir(path)
    file_path = os.path.join(path, file_name)
    if not os.path.exists(file_path):
        f = open(file_path, 'wb')
        print "downloading " + file_name + "......"
        for chunk in real_pic_r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        f.close()

def make_soup(url, tag, name):
    page = get_page(url)
    if None == page:
        return None
    soup = BeautifulSoup(page)
    what_we_got = soup.find_all(attrs={tag:name})
    return what_we_got

def get_page(url):
    try:
        page = s.get(url, headers=header_li[header_num], verify=False).text
    except requests.exceptions.ConnectionError:
        time.sleep(10)
        return None
    return page

def get_article_url(page_url):
    tag_li = make_soup(page_url, "class", "title")
    if None == tag_li:
        print "err exist!"
        return 
    for tag in tag_li:
        if (False == tag.a.has_key('title')):
            continue
        print tag.a['title']
        print tag.a['href']
        title = tag.a['title'] + "--" + tag.a['href']
        save_pic_info(title)
        article_url = tag.a['href']
        get_img_url(article_url)
        time.sleep(3)

def get_img_url(url):
    tag_li = make_soup(url, "class", "topic-figure cc")
    if None == tag_li:
        print "err exist!"
        return
    for tag in tag_li:
        print tag.img['src']
        save_pic_info(tag.img['src'])
        #save_pic(tag.img['src'])
    
for index in range(0, max_page):
    num = 25*index
    header_num = index % 5
    url = page_url + str(num)
    print url
    save_pic_info(url)
    get_article_url(url)
