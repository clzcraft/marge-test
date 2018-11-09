# -*- coding:utf8 -*-
import requests
from bs4 import BeautifulSoup
import re
import os

header = {
    'Referer': 'http://www.mmjpg.com/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3269.3 Safari/537.36'
}

url = 'http://www.mmjpg.com/'

#将url添加页码,限定在一个页码，打开可循环。
def data_num(url, parms, page):
    url4 = []
    for i in range(1, page+1):
        if i == 1:
            url5 = url
        else:
            url5 = url + parms + str(i)
        url4.append(url5)
    url3 = url4[-1]
    return url3

#将页面使用bs4处理
def data_temp(url2):
    data_b = requests.get(url2)
    data_b.encoding = 'utf-8'
    data_b = BeautifulSoup(data_b.content)
    return data_b
#处理基础页面跳转的图集名称和连接
def data_link(url):
    m, n = [], []
    data_c = data_temp(url)
    data_c = data_c.find('div', class_='pic')
    data_c = data_c.find_all('li')
    for i in data_c:
        data_c = i.find('span')
        data_c = re.search('.*href=\"(.*)\".*target.*\>(.*)\<\/a>', str(data_c))
        m.append(data_c.group(1))
        n.append(data_c.group(2))
    data_c = dict(zip(m, n))
    return data_c

#获取每张图的跳转和分析 主体
def data_web(url):
    w = data_link(url)
    for i in list(w.keys()):
        #总图片个数str类型
        #x = data_page(i)
        y = w[i]
        data_mkdir(y)
        #每个下载地址的连接y属于目录名下载到相应目录下
        #for j in range(1, int(x)):
        #现在只限定下载9张，若开放上面就是下载全部存在的图片
        for j in range(1, 20):
            data_w = data_num(i, '/', j)
            data_w =data_link_link(data_w)
            data_down(data_w, y)

#图片页数
def data_page(web):
    data_r = data_temp(web)
    data_r = data_r.find('div', class_='page')
    data_r = data_r.find_all('a')[-2]
    data_r = data_r.string
    return data_r
#下载地址
def data_link_link(web):
    data_l = data_temp(web)
    data_l = data_l.find('div', class_='content')
    data_l2 = data_l.img['data-img']
    return data_l2

#创建人物图片目录
def data_mkdir(x):
    if not os.path.exists('C:/Users/clzcr/Downloads/temp/' + x):
        os.makedirs('C:/Users/clzcr/Downloads/temp/' + x)
    else:
        print("文件已经创建")

#将连接地址下载并保存：
def data_down(url, y):
    a = requests.session()
    a = a.get(url, headers=header)
    dir_root = 'C:/Users/clzcr/Downloads/temp/' + y + '/'
    dir_y = dir_root + url.split('/')[-1]
    print(dir_y)
    with open(dir_y, 'wb') as file:
        file.write(a.content)

if __name__ == '__main__':
    onepage = data_num(url, 'home/', 3)
    data_web(onepage)
