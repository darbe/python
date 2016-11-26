# -*- coding: utf-8 -*- 
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
import requests
logger = logging.getLogger("log")
class Item:
    def __init__(self,uid,uname,utype,ufrom,gid,gname,sex):
        self.uid=uid
        self.uname=uname
        self.utype=utype
        self.ufrom=ufrom
        self.gid=gid
        self.gname=gname
        self.sex=sex
    def printItem(self):
        print 'uid:',self.uid,' uname:',self.uname,' utype:',self.utype,' ufrom:',self.ufrom,' gid:',self.gid+' gname:',self.gname,' sex:',self.sex
class Follower :
    def __init__(self,session):
        self.headers = session.headers
        self.opener = session.opener
        self.uniqueid = session.uniqueid
        self.userDomain = session.userDomain
        self.followers = []
        self.totalFollower = 0
    def findUid(self):
        hotUrl = 'http://weibo.com/feed/hot?leftnav=1&page_id=102803_ctg1_1760_-_ctg1_1760'
        request  = urllib2.Request(  
                        url = hotUrl,  
                        headers = self.headers  
                )  
        response = self.opener.open(request) 
        content = response.read()
        content = content.replace('\/','/').replace('\\n','\n').replace('\\r','\r').replace('\\t','\t')
        Pattern = re.compile('FM.view\(\{([^\}]+)\}\)')
        soup = BeautifulSoup(content,'html.parser')
        elements = soup.find_all('script')
        eleID = ''
        html = ''
        for ele in elements:
            text = ele.get_text()
            if '''"domid":"plc_main"''' in text :
                data = Pattern.search(text).group(1)
                index1 = data.find('div id')
                index2 = data.find('</div>',index1)
                eleID = data[index1+9:index2-3]
                print eleID
            if len(eleID) > 0 and eleID in text:
                index = text.find('html')
                html = text[index+6:len(text)-9]
        ofile = open('hot.html','w')
        ofile.write(content)
        ofile.close()
        return self.getInfo(html,0)
    def getAllFollower(self):
        followerUrl = 'http://weibo.com/5617266263/follow?rightmod=1&wvr=6'
        self.getFollower(followerUrl )
        i = 1
        while True:
            if len(self.followers ) >= int(self.totalFollower):
                break
            i = i+1
            leftUrl = 'http://weibo.com/p/100505'+self.uniqueid+'/myfollow?t=1&pids=Pl_Official_RelationMyfollow__96&cfs=&Pl_Official_RelationMyfollow__96_page='+str(i)+'#Pl_Official_RelationMyfollow__96'
            self.getFollower(leftUrl)
        print 'you have listen ', len(self.followers ) 
    def getFollower(self,followerUrl):
        
        request  = urllib2.Request(  
                        url = followerUrl,  
                       #data = formData,  
                        headers = self.headers  
                )
        response = self.opener.open(request) 
        content = response.read()
        ofile = open('tmp.html','w')
        ofile.write(content)
        ofile.close()
        content = content.replace('\/','/').replace('\\n','\n').replace('\\r','\r').replace('\\t','\t')
        Pattern = re.compile('FM.view\(\{([^\}]+)\}\)')
        soup = BeautifulSoup(content,'html.parser')
        elements = soup.find_all('script')
        eleID = ''
        html = ''
        for ele in elements:
            text = ele.get_text()
            if '''"domid":"Pl_Official_RelationMyfollow''' in text :
                index = text.find('html')
                html = text[index+6:len(text)-9]
        ofile = open('hot.html','w')
        ofile.write(content)
        ofile.close()
        soup = BeautifulSoup(html,'html.parser')
        flag = 0
        if flag == 0 :
            member_box = [u'\\"member_box\\"']
            WB_text = [u'\\"WB_text']
            member_li = [u'\\"member_li']
            classAttr = [u'\\"WB_cardwrap']
        else :
            WB_info = ['WB_info']
            WB_text = ['WB_text']
            classAttr = [u'WB_cardwrap', u'WB_feed_type', u'S_bg2', u'']
        divs = soup.find_all('div',attrs = {'class': classAttr})
        for div  in divs:
            box = div.div.div.find('div',attrs = {'class': member_box})
            if self.totalFollower == 0:
                self.totalFollower = div.div.div.div.div.div.span.em.get_text()
            uls = box.find('ul')
            lis =  uls.find_all('li',attrs = {'class':  member_li})
            for li in lis:
                data = li.attrs['action-data']
               # print data
                index = data.find('gid')
                index1 = data.find('&',index)
                gid = data[index+4:index1]
                index = data.find('gname')
                index1 = data.find('&',index)
                gname = data[index+6:index1]
                index = data.find('sex')
                sex = data[index+4]
                #print gid, gname,sex
                li_a = li.find('div',attrs = {'class':  [u'\\"title']}).a
                #uname =  li_a['title']
                num = re.compile('\d+')
                uid = num.findall(li_a['usercard'])[0]
                uname = li_a.get_text().strip('\t\n ').strip()
                utype =  li.find('div',attrs = {'class':  [u'\\"text']}).get_text().strip('\t\n ').strip()
                from_a = li.find('div',attrs = {'class':  [u'\\"info_from']})
                ufrom =  from_a.get_text().strip('\t\n ').strip()
                #print from_a.a.get_text()
                item = Item(uid,uname,utype,ufrom,gid,gname,sex)
                self.followers.append(item)
                item.printItem()
       

    def findAllMid(self):
        mids = self.findUid()
        if not mids:
            print 'error'
            return
        end_id = mids[0] 
        min_id = mids[1]
        current_page = 1
        for i in range(10):
            print 'page-----------> ', i+1  
            for j in range(10):
                pre_page = i+1
                page = i+1
                pagebar = j
                randnum =  int( time.time() * 1000)
                ajaxUrl = 'http://weibo.com/aj/hot/list?ajwvr=6&'+'pre_page='+str(pre_page)+'&page='+str(page)+'&end_id='+str(end_id)+'&min_id='+str(min_id)+'&leftnav=1'+'&page_id=102803_ctg1_1760_-_ctg1_1760'+ '&pagebar='+str(pagebar)+'&tab=home'+'&current_page='+str(current_page)+'&__rnd='+str(randnum)#'1479974358995'
                #print ajaxUrl
                current_page += 1
                #print ajaxUrl
                if current_page % 11 == 0:
                    min_id = self.ajaxLoad(ajaxUrl)[1]
            ajaxUrl = 'http://weibo.com/aj/hot/list?ajwvr=6&'+'pre_page='+str(pre_page)+'&page='+str(page+1)+'&end_id='+str(end_id)+'&min_id='+str(min_id)+'&leftnav=1'+'&page_id=102803_ctg1_1760_-_ctg1_1760&'+'pids=Pl_Content_NewMixFeed'+'&current_page='+str(current_page)+'&since_id='+'&__rnd='+str(randnum)#'1479974358995'
            #print ajaxUrl
            current_page += 1
            min_id = self.ajaxLoad(ajaxUrl)[1]
            #print ajaxUrl

    def ajaxLoad(self,ajaxUrl=''): 
        #ajaxUrl = 'http://weibo.com/aj/hot/list?ajwvr=6&pre_page=1&page=1&end_id=4044962406312861&min_id=4045111517919234&leftnav=1&page_id=102803_ctg1_1760_-_ctg1_1760&pagebar=4&tab=home&current_page=5&__rnd=1480043588138'
        request  = urllib2.Request(  
                        url = ajaxUrl,  
                       #data = formData,  
                        headers = self.headers  
                )
        #print ajaxUrl 
        response = self.opener.open(request) 
        content = response.read()
        ofile = open('ajax.html','w')
        ofile.write(content)
        ofile.close()
        jsonData = json.loads(content)
        html = jsonData['data']
        return self.getInfo(html,1)
    def getInfo(self,html,flag ):
        soup = BeautifulSoup(html,'html.parser')
        if flag == 0 :
            WB_info = [u'\\"WB_info\\"']
            WB_text = [u'\\"WB_text']
            classAttr = ['\\"WB_cardwrap']
        else :
            WB_info = ['WB_info']
            WB_text = ['WB_text']
            classAttr = [u'WB_cardwrap', u'WB_feed_type', u'S_bg2', u'']
        divs = soup.find_all('div',attrs = {'class': classAttr})
        first = True
        mid = ''
        endid = ''
        for div in divs:
            if 'mid' not in div.attrs:
                continue
            num = re.compile('\d+')
            mid = div.attrs['mid']
            mid = num.findall(mid)[0]
            if first:
                endid = mid
                first = False
            ouid = div.attrs['tbinfo']
            ouid = num.findall(ouid)[0]
            info = div.find('div',attrs = {'class':WB_info})
            uname = info.a['nick-name']
            index = uname.find('"') 
            if index != -1:
                index1 = uname.find('\\',index)
                uname =  uname[index+1:index1]
            print mid, ouid,uname#[2:-2]
            self.follow(ouid,uname)
            time.sleep(10)

        minid = mid
        return [endid, minid]
         
    def follow(self,uid = '', nick = ''):
        randnum =  int( time.time() * 1000)
        sendUrl = 'http://weibo.com/aj/f/followed?ajwvr=6&__rnd='+str(randnum)
        headers = self.headers
        headers['Referer'] = 'http://www.weibo.com/u/'+self.uniqueid+'/home'+self.userDomain[1:self.userDomain.index('&')]
        postData = {  
            'uid':uid,
            'objectid':'',
            'f':'1',
            'extra':'',
            'refer_sort':'card',
            'refer_flag':'followed',
            'refer_flag':'0000020001_',
            'location':'v6_content_home',
            'oid':uid,
            'wforce':'1',
            'nogroup':'false',
            'fnick': nick,
            'template':'1',
            'refer_lflag':'0000010005_',
            '_t':'0'
        } 
        formData = urllib.urlencode(postData) 
        request  = urllib2.Request(  
                        url = sendUrl,  
                        data = formData,  
                        headers = headers  
                )  
        response = self.opener.open(request) 
        content = response.read()
        ofile = open('follow.html','w')
        ofile.write(content)
        ofile.close()
        jsonData = json.loads(content)
        if jsonData['code'] == '100000':
            print 'follow ok'
            print jsonData['data']['fnick']
        else :
            print 'follow error',content[:500],jsonData['msg']
    def unfollow(self,info):
        randnum =  int( time.time() * 1000)
        unfollowUrl = 'http://weibo.com/aj/f/unfollow?ajwvr=6&__rnd='+str(randnum)
        headers = self.headers
        headers['Referer'] = 'http://www.weibo.com/u/'+self.uniqueid+'/home'+self.userDomain[1:self.userDomain.index('&')]
        postData = {  
            'refer_sort':'relationManage',
            'location':'page_100505_myfollow',
            'refer_flag':'unfollow',
            'uid':info.uid,
            #'profile_image_url:http://tva2.sinaimg.cn/crop.0.0.300.300.50/7a273328jw8f1001nng6qj208c08cta3.jpg
            'gid':info.gid,
            'gname':info.gname,
            'screen_name':info.uname,
            'sex':info.sex,
            '_t':'0'
        } 
        formData = urllib.urlencode(postData) 
        request  = urllib2.Request(  
                        url = unfollowUrl,  
                        data = formData,  
                        headers = headers  
                )  
        response = self.opener.open(request) 
        content = response.read()
        ofile = open('follow.html','w')
        ofile.write(content)
        ofile.close()
        jsonData = json.loads(content)
        if jsonData[u'code']== u'100000':
            self.followers.remove(info)
            print 'unfollow ok'
        else:
            print 'unfollow error',jsonData,jsonData['msg']
    def unfollowAll(self):
        #self.getAllFollower()
        print len(self.followers)
        for follower in  self.followers :
            time.sleep(1)
            self.unfollow( follower)
        print len(self.followers )
        return len(self.followers )

    def test(self):
        info = Item('5884957483','MogOnline','','','0','未分组','f')
        self.unfollow(info)
