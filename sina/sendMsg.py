# -*- coding: utf-8 -*- 
import urllib  
import urllib2
import time
import random
import os
import json
import config
import re
import os
import base64
class SendMsger :
    def __init__(self,session):
        self.headers = session.headers
        self.opener = session.opener
        self.uniqueid = session.uniqueid
        self.userDomain = session.userDomain
    def getImageID(self,imagePath):
        name = os.path.basename(imagePath)
        try:
            imageData = open(imagePath,'rb')
            uploadUrl =  'http://picupload.service.weibo.com/interface/pic_upload.php?rotate=0&app=miniblog&s=json&mime=image/jpeg&data=1&wm='
            request  = urllib2.Request(  
                   url =  uploadUrl,  
                   data = imageData.read()
                ) 
            response = self.opener.open(request) 
            content = response.read() 
            jsonData = re.search( '{.*}}',content).group(0)
            result = json.loads(jsonData)
            code = result["code"]
            if code == "A00006":
                pid = result["data"]["pics"]["pic_1"]["pid"]
                print u'image upload ok--->',name
                return pid
            else :
                print u'image upload fail----> ',name 
        except Exception as e:
            print e 
            print u'image upload fail exception----> ',name 
        return None

    def sendMessge(self , msg, isimage =  False , imagePath= ''):
        randnum =  int( time.time() * 1000)
        sendUrl = 'http://www.weibo.com/aj/mblog/add?ajwvr=6&__rnd='+str(randnum)
        headers = self.headers
        headers['Referer'] = 'http://www.weibo.com/u/'+self.uniqueid+'/home'+self.userDomain[1:self.userDomain.index('&')]
        postData = {  
            'location':'v6_content_home',
            "appkey": '',
            'style_type':'1',
            "pic_id": '',
            'text':msg,
            'pdetail':'',
            'rank':'0',
            'module':'stissue',
            'pub_source':'main_',
            'pub_type':'dialog',
            "_t":'0' 
        } 
        if isimage :
            if len(imagePath) == 0 :
                print 'image path invaild send image error'
            else:
                imageid = self.getImageID(imagePath)
                if imageid :
                     postData['pic_id'] = imageid
        formData = urllib.urlencode(postData) 
        request  = urllib2.Request(  
                        url = sendUrl,  
                        data = formData,  
                        headers = headers  
                )  
        response = self.opener.open(request) 
        content = response.read()
        jsonData = json.loads(content)

        if 'code' not in jsonData:
            print 'send fail unknown error'
            return False
        if jsonData['code'] ==  config.SENDSUCC:
            print '发送成功 msg: ',msg 
            return True
        else :
            print  '发送失败 :' ,jsonData['msg'].split('\n')[2]

           # print jsonData['msg'].split(u'。')[0]+u'。'
            return False
        #ofile = open("send.html","w+")  
        #ofile.write(content)  
        #ofile.close()
        