# -*- coding: utf-8 -*-

import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup
import json
import random
import time
from datetime import datetime, timedelta
import os


# 传入cookie
def GetHeaders(cookie):
    cookie = cookie
    User_Agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    headers = {'User-Agent': User_Agent, 'cookie': cookie}
    return headers


# 创建文件路径
def CreateFile(path):
    if os.path.exists(path):
        print('You forget to RENAME THE FILE!!!')
        exit()
    else:
        file = open(path, 'w', encoding='utf-8')
    return file
"""
def ReadFile(path):
    file=open(path,'r',encoding='utf-8')
    return file
"""


# 获取初始url
def GetUrl(keyword, starttime, endtime):
    url = 'http://s.weibo.com/weibo/' + \
        str(keyword)+'&typeall=1&suball=1&timescope=custom:' + \
        str(starttime)+':'+str(endtime)+'&page=1'
    return quote(url, safe='/:?=')


# 获取解码后的页面soup
def GetSoup(url, headers):
    request = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(request)
    soup = BeautifulSoup(html.read(), "html.parser")
    lines = soup.prettify().splitlines()
    for line in lines:
        if line.startswith('  STK && STK.pageletM && STK.pageletM.view({"pid":"pl_weibo_direct"'):
            n = line.find('html":"')
            if n > 0:
                j = line[n + 7: -3].replace("\\n", "\n").replace("\\t", "\t").replace(
                    '\\"', '\"').replace('\/', '/')  # .replace('\\\\','\\')
                soup = BeautifulSoup(j, "html.parser")
    return soup


# 获取微博页数
def GetPagenum(soup):
    pages = soup.find("div", class_="layer_menu_list W_scroll")
    page_num = 0
    try:
        for page in pages.children:
            for num in page.children:
                page_num = page_num+1
    except Exception as e:
        pass
    else:
        pass
    finally:
        pass
    print("toatl pages："+str(page_num))
    return page_num


# 获取微博内容并解码
def GetContents(soup, file_content, file_info):
    contents = soup.findAll(class_="comment_txt")
    names = soup.find_all('a', class_='name_txt W_fb')
    reads = soup.findAll(class_='feed_action_info feed_action_row4')
    i = 0
    alltxt = ''
    infotxt = ''
    for con in contents:
        for child in con.children:
            try:
                a = str(child.string)
                a = a.strip()
                a = a.replace("\n", '').replace("\t", '').replace('None', '')
                x = json.loads('{"foo":"%s"}' % a)
                x = x['foo']
                alltxt = alltxt+x
            except Exception as e:
                pass
            else:
                pass
            finally:
                pass
        alltxt = alltxt+'\n'
        nickname = names[i]['title']
        nickname = nickname.strip()
        t = json.loads('{"foo":"%s"}' % nickname)
        t = t['foo']
        infotxt = infotxt+str(t)+'\t'
        for li in reads[i].find_all('li'):
            s = li.get_text().strip().replace('\n', '')
            t = json.loads('{"foo":"%s"}' % s)
            t = t['foo']
            infotxt = infotxt+str(t)+'\t'
        infotxt = infotxt+'\n'
        i += 1

    print('Gain '+str(len(alltxt))+'datas')
    file_content.write(alltxt)
    file_info.write(infotxt)


def GetPages(page_num, url, headers, file_content, file_info):
    urls = []
    num = page_num+1
    for i in range(1, num):
        urls.append(url.replace("page=1", "page="+str(i)))
    j = 0
    for u in urls:
        soup = GetSoup(u, headers)
        GetContents(soup, file_content, file_info)
        j = j+1
        print(str(j)+"pages Done!")
        se = random.randint(20, 100)
        print(str(se)+"s later.")
        time.sleep(se)
    se = random.randint(20, 100)
    print(str(se)+"later.")
    time.sleep(se)


# 返回日期列表
def datelist(start, end):
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')
    result = []
    curr_date = start_date
    while curr_date <= end_date:
        day = curr_date.strftime('%Y-%m-%d')
        result.append(str(day))
        curr_date = curr_date + timedelta(1)
    return result


# 返回最终结果
def GetResults(result, keyword, headers, file_content, file_info):
    for day in result:
        url = GetUrl(keyword, day, day)
        soup = GetSoup(url, headers)
        # print(soup)
        page_num = GetPagenum(soup)
        GetPages(page_num, url, headers, file_content, file_info)
        print(str(day)+' done.\n')


if __name__ == '__main__':
    # keyword=input("请输入关键词：\n")
    # starttime=input("请输入开始时间（如2016-09-01）\n")
    # endtime=input("请输入开始时间（如2016-09-02）\n")
    # cookie=input("请输入浏览器cookie\n")
    starttime = "2016-09-01"
    endtime = "2016-10-31"
    result = datelist(starttime, endtime)
    # print(result)
    keyword = "大学 图书馆"
    cookie ='SINAGLOBAL=3352532472805.2163.1482110856449; wvr=6; WBStorage=2c466cc84b6dda21|undefined; login_sid_t=5b13a8623b10aef462171bda8745631a; _s_tentry=-; UOR=,,www.baidu.com; Apache=8028505545622.833.1482306288956; ULV=1482306288965:3:3:3:8028505545622.833.1482306288956:1482283982034; NSC_wjq_txfjcp_mjotij=ffffffff094113da45525d5f4f58455e445a4a423660; SCF=Ahiws7Pzdh8y6uVZQlmkak5vbXCgPBNY90YIPsCJcA7kzG84t25xDQex_VwGYwG7fC3n5sRXUGj9LBJnInr9MEo.; SUB=_2A251XkNhDeRxGeRN4lYX9S_OzzmIHXVWKjOprDV8PUNbmtAKLXXHkW82O7rpuXyuCFwIrZGtNxSCXz39mA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WheQnKJDqVMSKEHcDOJqPGH5JpX5K2hUgL.Foz01KBcSK2ESh-2dJLoI7De9gvWMJSPdcv.; SUHB=0A0IPKoal7w2JE; ALF=1513842353; SSOLoginState=1482306353; un=15605179129'
    headers = GetHeaders(cookie)
    file_content = CreateFile("20160901-20161031.txt")
    file_info = CreateFile("20160901-20161031(info).txt")
    GetResults(result, keyword, headers, file_content, file_info)
    file_content.close()
    file_info.close()
