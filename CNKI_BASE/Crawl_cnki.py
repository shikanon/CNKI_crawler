# -*- coding: cp936 -*-
import urllib,urllib2,cookielib,httplib,time,re,Parameters

def ToUtf(string):
    return string.decode('gbk').encode('utf8')

class CNKI:
    def search(self):
        #两个发送请求的主网页,知网需要两次发送请求,一次为参数请求,一次为返回页面请求
        url='http://epub.cnki.net/KNS/request/SearchHandler.ashx?action=&NaviCode=*&'
        url2='http://epub.cnki.net/kns/brief/brief.aspx?'
        
        #生成cookie
        cookie = cookielib.CookieJar()

        #创建一个新的opener来使用cookiejar
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie),urllib2.HTTPHandler)
        
        #构建头结构，模拟浏览器
        #httplib.HTTPConnection.debuglevel = 1
        hosturl='http://epub.cnki.net/kns/brief/result.aspx?dbprefix=scdb&action=scdbsearch&db_opt=SCDB'
        headers={'Connection':'Keep-Alive',
                 'Accept':'text/html,*/*',
                 'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36',
                 'Referer':hosturl}
        
        #通过chorme抓包获取提交参数,解析提交参数，CNKI为utf-8编码而非gbk编码
        #知网的参数编码是UTF8编码，所以中文需要先gbk解码再进行utf-8编码
        #再将参数url编码,编码顺序并不影响提交成果
        parameters=Parameters.parameters()
        postdata=urllib.urlencode(parameters)
        
        #构建第二次提交参数，不过貌似这些参数对返回值没有影响，尝试了修改keyValue和spvalue依然能正常返回
        query_string=urllib.urlencode({'pagename':'ASP.brief_result_aspx','DbCatalog':'中国学术文献网络出版总库',
                                       'ConfigFile':'SCDB.xml','research':'off','t':int(time.time()),
                                       'keyValue':'','dbPrefix':'SCDB',
                                       'S':'1','spfield':'SU','spvalue':'',
                                       })
        
        #实施第一步提交申请
        req=urllib2.Request(url+postdata,headers=headers)
        html=opener.open(req).read()
        with open('web1.html','w') as e:
            e.write(html)

        #第二步提交申请,第二步提交后的结果就是查询结果
        req2=urllib2.Request(url2+query_string,headers=headers)
        result2 = opener.open(req2)
        html2=result2.read()
        #打印cookie值,如果需要下载文章的话还需要登陆处理
        for item in cookie:
            print 'Cookie:%s:/n%s/n'%(item.name,item.value)
        with open('web2.html','w') as e:
            e.write(html2)
        
        print self.Regular(html)

        def Regular(self,html):
            reg='<a href="(.*?)"\ttarget'
            comlists=re.findall(re.compile(reg),html)
            return comlists

cnki=CNKI()
cnki.search()
