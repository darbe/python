# -*- coding: utf-8 -*- 
import urllib  
import urllib2
import time
import random
import os
import json
import config
import re
from bs4 import BeautifulSoup
from Session import Session
from item import WeiboItem
import sys
import logging
logger = logging.getLogger("log") 
reload(sys)
sys.setdefaultencoding('utf8')
class DeleteMsger :
    def __init__(self, session ):
        self.headers = session.headers
        self.opener = session.opener
        self.uniqueid = session.uniqueid
        self.userDomain = session.userDomain
        self.totalPage = 0
        self.weibos = []
    
    def deleteMsg(self,mid,pageID=''):
        delUrl = 'http://weibo.com/aj/mblog/del?ajwvr=6'
        headers = self.headers
        headers['Referer'] = 'http://weibo.com/'+self.uniqueid+'/profile?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page='+pageID
        postData = {  
            'mid':mid,
        }
        formData = urllib.urlencode(postData) 
        request  = urllib2.Request(  
                        url = delUrl,  
                        data = formData,  
                        headers = headers  
                )   
        response = self.opener.open(request) 
        content = response.read()
        #print content.decode('GB2312')
    def deleteAll(self):
        self.findAllMid()
        for weibo in self.weibos:
            info = '<------------------delete '+weibo.mid+' ------------------>'
            logger.info(info)
            self.deleteMsg(weibo.mid)
            time.sleep(1)

    
    def findAllMid(self):
        logger.debug('<------------------first page------------------>')
        self.findMid()
        self.loadCurrentLeft('0')
        self.loadCurrentLeft('1')

        for i in range(2,int(self.totalPage+1)):
        #for i in range(2,2):
            if i > self.totalPage:
                break
            info = '<------------------'+str(i)+'------------------>'
            logger.debug (info)
            self.findPage(str(i))
            self.loadOtherLeft(str(i),'0')
            self.loadOtherLeft(str(i),'1')
        info = 'you  have ' + str(len(self.weibos)) + ' weibos'
        logger.info(info) 
    def findPage(self,pageID):
        pageUrl = 'http://weibo.com/p/100505'+self.uniqueid+'/home?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page='+pageID+'#feedtop'
        headers = self.headers
        headers['Referer'] = 'http://weibo.com/u/'+self.uniqueid+'/home?topnav=1&wvr=6'
        postData = {  
            'rightmod':'1',
            'wvr':'6',
            'mod':'personnumber',
            'ajaxpagelet':'1',
            'ajaxpagelet_v6':'1',
            '__ref':'/u/'+self.uniqueid+'/home?'+self.userDomain[1:self.userDomain.index('&')],
            '_t':'FM_147913011455241'
        } 
        formData = urllib.urlencode(postData) 
        request  = urllib2.Request(  
                        url = pageUrl,  
                        data = formData,  
                        headers = headers  
                )  
        response = self.opener.open(request) 
        content = response.read()
        self.processHtml(content)
    def loadOtherLeft(self,pageID,pagebarID):
        leftUrl = 'http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page='+pageID+'&pagebar='+pagebarID+'&pl_name=Pl_Official_MyProfileFeed__22&id=100505'+self.uniqueid +'&script_uri=/'+self.uniqueid +'/profile&feed_type=0&pre_page='+pageID+'&domain_op=100505&__rnd=1479264049377'
        postData = { 
            'ajwvr':'6',
            'domain':'100505',
            'is_search':'0',
            'visible':'0',
            'is_all':'1',
            'is_tag':'0',
            'profile_ftype':'1',
            'page':pageID,
            'pagebar':pagebarID,
            'pl_name':'Pl_Official_MyProfileFeed__22',
            'id':'100505'+self.uniqueid,
            'script_uri':'/'+self.uniqueid+'/profile',
            'feed_type':'0',
            'pre_page':pageID,
            'domain_op':'100505',
            '__rnd':'1479264049377'
        } 
        referer = 'http://weibo.com/'+self.uniqueid+'/profile?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page='+pageID
        self.ajaxLoad(leftUrl,postData,referer,pagebarID)
    def loadCurrentLeft(self,pagebarID):
        sencodUrl = 'http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&rightmod=1&wvr=6&mod=personnumber&is_all=1&pagebar='+pagebarID+'&pl_name=Pl_Official_MyProfileFeed__22&id=100505'+self.uniqueid +'&script_uri=/'+self.uniqueid +'/profile&feed_type=0&page=1&pre_page=1&domain_op=100505&__rnd=1479260530683'
        postData = { 
            'ajwvr':'6',
            'domain':'100505',
            'rightmod':'1',
            'wvr':'6',
            'mod':'personnumber',
            'is_all':'1',
            'pagebar':'0',
            'pl_name':'Pl_Official_MyProfileFeed__22',
            'id':'100505'+self.uniqueid,
            'script_uri':'/'+self.uniqueid+'/profile',
            'feed_type':'0',
            'page':'1',
            'pre_page':'1',
            'domain_op':'100505',
            '__rnd':'1479199182376' 
        } 
        referer = 'http://weibo.com/'+self.uniqueid+'/profile?rightmod=1&wvr=6&mod=personnumber&is_all=1'
        self.ajaxLoad(sencodUrl,postData,referer,pagebarID)
    def ajaxLoad(self,sencodUrl,postData, referer,pagebarID):
        headers = self.headers
        headers['Referer'] = referer
        formData = urllib.urlencode(postData) 
        request  = urllib2.Request(  
                        url = sencodUrl,  
                        data = formData,  
                        headers = headers  
                )  
        response = self.opener.open(request) 
        content = response.read()
        #print '****',content
        jsonData = json.loads(content)
        html = jsonData['data']
        ofile = open('json.data','w+')
        ofile.write(html)
        ofile.close()
        if pagebarID == '1':
            index = html.find('currentPage')
            index = html.find('=',index)
            index0 = html.find('&',index)
            pages =  html[index+1:index0].strip()
            if len(pages) == 0:
                pages = '0'
            info = 'you  have ' + pages+ ' pages'
            logger.debug(info) 
            if self.totalPage == 0:
                index = html.find('countPage',index0)
                index = html.find('=',index)
                index0 = html.find('"',index)
                snum = html[index+1:index0]
                if len(snum.strip()) == 0:
                    self.totalPage = 0
                else:
                    self.totalPage =  int(snum)
    #print html
        self.getInfo(html,1)
            
    def findMid(self):
        delUrl = 'http://weibo.com/'+self.uniqueid+'/profile?rightmod=1&wvr=6&mod=personnumber&is_all=1'
        headers = self.headers
        headers['Referer'] = 'http://weibo.com/u/'+self.uniqueid+'/home'+self.userDomain[1:self.userDomain.index('&')]
        postData = {  
            'rightmod':'1',
            'wvr':'6',
            'mod':'personnumber',
            'ajaxpagelet':'1',
            'ajaxpagelet_v6':'1',
            '__ref':'/u/'+self.uniqueid+'/home'+self.userDomain[1:self.userDomain.index('&')],
            '_t':'FM_147913011455241'
        } 
        formData = urllib.urlencode(postData) 
        request  = urllib2.Request(  
                        url = delUrl,  
                        data = formData,  
                        headers = headers  
                )  
        response = self.opener.open(request) 
        content = response.read()
        ofile = open('weibo.html','w+')
        ofile.write(content)
        ofile.close()
        self.processHtml(content)
    def processHtml(self,content):
        content = content.replace('\/','/').replace('\\n','\n').replace('\\r','\r').replace('\\t','\t')
        Pattern = re.compile('FM.view\(\{([^\}]+)\}\)')
        soup = BeautifulSoup(content,'html.parser')
        elements = soup.find_all('script')
        html = ''
        for ele in elements:
            text = ele.get_text()
            if '''"domid":"Pl_Official_MyProfileFeed__22"''' in text :
                index = text.find('html')
                html = text[index+6:len(text)-9]
        self.getInfo(html,0)
    def getInfo(self,html,flag ):
        soup = BeautifulSoup(html,'html.parser')
        if flag == 0 :
            WB_from = [u'\\"WB_from']
            WB_text = [u'\\"WB_text']
            classAttr = ['\\"WB_cardwrap']
        else :
            WB_from = ['WB_from']
            WB_text = ['WB_text']
            classAttr = [u'WB_cardwrap', u'WB_feed_type', u'S_bg2', u'']
        divs = soup.find_all('div',attrs = {'class': classAttr})
        for div in divs:
            if 'mid' not in div.attrs:
                continue
            mid = div.attrs['mid']
            #left = mid.find('=')
            #right = mid.find('\\',left)
            #print mid
            #mid = mid[left+1:right]
            num = re.compile('\d+')
            mid = num.findall(mid)[0]
            info = div.find('div',attrs = {'class':WB_from}).get_text()
            info.strip('\t\n ')
            infos = info.split()
            #print infos
            weibo = div.find('div',attrs = {'class':WB_text})
            text = weibo.get_text().strip('\t\n ')
            link = ''
            if weibo.a:
                link = weibo.a['href']
            item = WeiboItem(mid,infos[0],infos[1],infos[3],text,link)
            item.printInfo()
            print "\n\n"
            self.weibos.append(item)





    
        
        
         
        


#s = Session()
#d = DeleteMsger(s)
#d.getInfo2('')
