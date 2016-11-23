# -*- coding: utf-8 -*- 
import urllib  
import urllib2
import time
import random
import os
import re


class forwardMsger:
    def __init__(self,session):
        self.headers = session.headers
        self.opener = session.opener
        self.uniqueid = session.uniqueid
        self.userDomain = session.userDomain
    def forwardMessge(self , msg, mid):
        randnum =  int( time.time() * 1000)
        forwardUrl = 'http://weibo.com/aj/v6/mblog/forward?ajwvr=6&domain=100505&__rnd='+str(randnum)
        print forwardUrl
        headers = self.headers
        headers['Referer'] = 'http://weibo.com/u/i'+self.uniqueid+'/home?'+self.userDomain[1:self.userDomain.index('&')]
        postData = {  
            'pic_src':'v6_content_home',
            'pic_id': '',
            'appkey':'',
            'mid':  mid,
            'style_type':'1',
            'mark':'',
            'reason':msg,
            'location':'v6_content_home',
            'pdetail':'',
            'module':'',
            'page_module_id':'',
            'refer_sort':'',
            'rank':'0',
            'rankid':'',
            'group_source':'group_all', 
            '_t':'0'
        }  
        formData = urllib.urlencode(postData)
        request  = urllib2.Request(  
                        url = forwardUrl,  
                        data = formData,  
                        headers = headers  
                ) 
        print request 
        response = self.opener.open(request) 
        print  response
        content = response.read()
        ofile = open("w.html","w+")  
        ofile.write(content)  
        ofile.close()



