# -*- coding: cp936 -*-
#SU主题,TI篇名,KY关键词,AB摘要,FT全文
#通过chorme抓包获取提交参数,解析提交参数，CNKI为utf-8编码而非gbk编码
#知网的参数编码是UTF8编码，所以中文需要先gbk解码再进行utf-8编码
import time

def ToUtf(string):
    return string.decode('gbk').encode('utf8')

search={'SU':'分异','TI':'分异'}
DbCatalog=ToUtf('中国学术文献网络出版总库')
magazine=ToUtf('地理学报')
times=time.strftime('%a %b %d %Y %H:%M:%S')+' GMT+0800 (中国标准时间)'

parameter={'ua':'1.21',
            'PageName':'ASP.brief_result_aspx',
            'DbPrefix':'SCDB',
            'DbCatalog':DbCatalog,
            'ConfigFile':'SCDB.xml',
            'db_opt':'CJFQ,CJFN,CDFD,CMFD,CPFD,IPFD,CCND,CCJD,HBRD',
            'base_special1':'%',
            'magazine_value1':magazine,
            'magazine_special1':'%',
            'his':'0',
            '__':times}

def BuildQuery(value):
    par={'txt_1_relation':'#CNKI_AND','txt_1_special1':'='}
    i=0
    for v in value:
        i=i+1
        par['txt_%d_sel'%i]=v
        par['txt_%d_value1'%i]=ToUtf(value[v])
        par['txt_%d_relation'%i]='#CNKI_AND'
        par['txt_%d_special1'%i]='='
    return par

def parameters():
    parameters=dict(parameter,**BuildQuery(search))
    return parameters
