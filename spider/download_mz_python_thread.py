#!/usr/bin/env python
# coding: utf-8
# author: markbug
# date  : 2015-09-22
# ver   : 1.0

import os,sys
import threading
import urllib
import urllib2
from bs4 import BeautifulSoup

url_base =  "http://www.maiziedu.com"

url_start = "http://www.maiziedu.com/course/python/"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:32.0) Gecko/20100101 Firefox/32.0'}

def get_save_path(name):
    path = os.getcwd()
    path = os.path.join(path,name)
    if not os.path.exists(path):
        os.mkdir(path)
    print "path [%s]" % path
    return path

def get_lesson_list():
    py_lesson_list = []

    request = urllib2.Request(url_start, headers = headers)
    r = urllib2.urlopen(request)
    soup = BeautifulSoup(r.read())

    for li_tag in soup.find_all("div", "artc-bt"):
        if li_tag.find_all('a'):
            url_tag = li_tag.a['href']
            py_lesson_list.append(url_base + url_tag)
    
    print len(py_lesson_list)
    return py_lesson_list

def get_lesson_name():
    py_name_list = []
    
    request = urllib2.Request(url_start, headers = headers)
    r = urllib2.urlopen(request)
    soup = BeautifulSoup(r.read())

    for li_tag in soup.find_all("div", "artc-bt"):
        if li_tag.find_all('a'):
            title_tag = li_tag.a['title']
            py_name_list.append(title_tag)
    print len(py_name_list)
    return py_name_list

'''
def get_lesson_url():#(lesson_name, lesson_url):
    #lesson_url_list = get_lesson_list()
    #lesson_name_list = get_lesson_name()

    #for index in range(len(lesson_url_list)):
    #    lesson_url = lesson_url_list[index]
    #    lesson_name = lesson_name_list[index]
        lesson_url_temp = []
        
        path = get_save_path(lesson_name)

        print "index[%d] %s" % (index, lesson_url)
        print lesson_name
        request = urllib2.Request(lesson_url, headers = headers)
        r = urllib2.urlopen(request) 
        soup = BeautifulSoup(r.read())
        
        play_tag = soup.find_all("div", "playlist scroll-pane")
        for li_tag in play_tag[0].find_all('li'):
            url_temp = li_tag.a['href']
            url = url_base + url_temp
            lesson_url_temp.append(url)
            download_lesson(url, path)
''' 

def get_video_url(lesson_name, lesson_url):
    lesson_url_temp = []
       
    path = get_save_path(lesson_name)

    print "index[%d] %s" % (index, lesson_url)
    print lesson_name
    request = urllib2.Request(lesson_url, headers = headers)
    r = urllib2.urlopen(request) 
    soup = BeautifulSoup(r.read())
        
    play_tag = soup.find_all("div", "playlist scroll-pane")
    for li_tag in play_tag[0].find_all('li'):
        url_temp = li_tag.a['href']
        url = url_base + url_temp
        lesson_url_temp.append(url)
        download_lesson(url, path)


#下载课程视频
def download_lesson(lesson_url, path):
    request = urllib2.Request(lesson_url, headers = headers)
    r = urllib2.urlopen(request)
    soup = BeautifulSoup(r.read()) 

    video_tag = soup.find_all("video")
    video_url = video_tag[0].source['src']
    #video_name = 
    #print video_tag
    print video_url
    
    filename_base = os.path.basename(video_url)
    filename = path + "/" + filename_base
    
    if(True == os.path.exists(filename)):
        print "file has been download!"
    else:
        urllib.urlretrieve(video_url, filename)
        print "download ok (%s) " % filename_base

# main process
if __name__=="__main__":
    threads = []

    lesson_url_list = get_lesson_list() 
    lesson_name_list = get_lesson_name()
    if len(lesson_url_list) != len(lesson_name_list):
        print "err: lesson url(%d) name(%d) " %(len(lesson_url_list), len(lesson_name_list))
    
    for index in range(len(lesson_url_list)):
        lesson_url = lesson_url_list[index]
        lesson_name = lesson_name_list[index]

        print "start to dowload lesson -- %s" % lesson_name
        #get_video_url(lesson_name, lesson_url)
        #threads.append(t)
        t = threading.Thread(target = get_video_url, args = (lesson_name, lesson_url))
        threads.append(t)
    
    for index in range(len(lesson_url_list)):  
        threads[index].start()

    for index in range(len(lesson_url_list)):
        threads[index].join()

    print "all file download ok !"
