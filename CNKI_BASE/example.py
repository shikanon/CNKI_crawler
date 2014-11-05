# -*- coding: cp936 -*-
#author:雪之忆
#---------------------

import HTMLParser
import urlparse
import urllib
import urllib2
import cookielib
import string
import re
import time
import httplib
import Cookie
def readtxt(path):
    url=[]
    with open(path,'r') as txt:
        url=txt.readlines()
    return url
'''登陆网页，读取网页'''
hosturl='http://www.cnki.net/'
#生成cookie
httplib.HTTPConnection.debuglevel = 1
cookie = cookielib.CookieJar()

#创建一个新的opener来使用cookiejar
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie),urllib2.HTTPHandler)
#post地址
posturl='http://epub.cnki.net/kns/brief/result.aspx?dbprefix=scdb&action=scdbsearch&db_opt=SCDB'
#构建头结构，模拟浏览器
headers={'Connection':'Keep-Alive',
         'Accept':'text/html,*/*',
         'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36',
         'Referer':posturl}
#通过chorme抓包获取postdata

#知网的参数编码是UTF8编码，所以中文需要先gbk解码再进行utf-8编码
DbCatalog='中国学术文献网络出版总库'.decode('gbk').encode('utf8')
magazine='地理学报'.decode('gbk').encode('utf8')
txt='分异'.decode('gbk').encode('utf8')
times=time.strftime('%a %b %d %Y %H:%M:%S')+' GMT+0800 (中国标准时间)'
parameters={'ua':'1.21',
            'PageName':'ASP.brief_result_aspx',
            'DbPrefix':'SCDB',
            'DbCatalog':DbCatalog,
            'ConfigFile':'SCDB.xml',
            'db_opt':'CJFQ,CJFN,CDFD,CMFD,CPFD,IPFD,CCND,CCJD,HBRD',
            'base_special1':'%',
            'magazine_value1':magazine,
            'magazine_special1':'%',
            'txt_1_sel':'SU',
            'txt_1_value1':txt,
            'txt_1_relation':'#CNKI_AND',
            'txt_1_special1':'=',
            'his':'0',
            '__':times}
postdata=urllib.urlencode(parameters)

query_string=urllib.urlencode({'pagename':'ASP.brief_result_aspx','DbCatalog':'中国学术文献网络出版总库',
                               'ConfigFile':'SCDB.xml','research':'off','t':int(time.time()),
                               'keyValue':'隔离','dbPrefix':'SCDB',
                               'S':'1','spfield':'SU','spvalue':'隔离',
                               })
#发送请求


url='http://epub.cnki.net/KNS/request/SearchHandler.ashx?action=&NaviCode=*&'
url2='http://epub.cnki.net/kns/brief/brief.aspx?'
#需要两步提交，第一部提交请求，第二步下载框架
req=urllib2.Request(url+postdata,headers=headers)
html=opener.open(req).read()


req2=urllib2.Request(url2+query_string,headers=headers)

#print req.get_header(),req.header_items()
#打开网页，登陆成功
result2 = opener.open(req2)

html2=result2.read()

##with open('web2.html','w') as e:
##    e.write(html2)

def Regular(html):
    reg='<a href="(.*?)"\ttarget'
    comlists=re.findall(re.compile(reg),html)
    return comlists

t=Regular(html2)
print t  
