# -*- coding: utf-8 -*- 
import urllib  
import urllib2
import cookielib  
import re  
import json
import rsa
import binascii 
import  base64 
import urlparse  
import random
import config
import time  
import urlparse
import os 
from Session import Session
from bs4 import BeautifulSoup
class Item :
    def __init__(self):
        self.count = 0.0
        self.theme = ''
        self.url = ''
    def __repr__(self):
        return repr((self.count, self.theme, self.url))
class SinaLogin :
    def __init__ (self,username,userpasswd,proxyUrl = None): 
        self.cookie = cookielib.CookieJar()    
        cookie_support = urllib2.HTTPCookieProcessor(self.cookie) 
        if not proxyUrl:
            proxy = {'http':proxyUrl}
            proxy_support = urllib2.ProxyHandler(proxy) 
            self.opener = urllib2.build_opener(proxy_support,cookie_support, urllib2.HTTPHandler)  
        self.opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)  
        urllib2.install_opener(self.opener)
        self.userName = username
        self.userPasswd = userpasswd
        self.jsonData = None
        self.uniqueid = ''
        self.userDomain = ''
        self.success = False
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'}
        #self.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0'}
        if not self.getServerData(config.PRELOGINURL):
            print 'prelogin error'
            exit(config.ERRORCODE)
        print 'prelogin ok  ------------------>'

    def getServerData(self,preLoginUrl):  
        content = urllib2.urlopen(config.PRELOGINURL).read()  
        elementPattern = re.compile(r'({[^{]+?})')
        try:  
            data = elementPattern.search(content)
            if not data :
                print 'sevice NULL'
                return False
            infor  = data.group(1)
            self.jsonData = json.loads(infor)
            return True 
        except:  
            print 'Get severtime error!'  
            return False
     
    def getPassword(self): 
        rsaPublickey = int(self.jsonData['pubkey'], 16)  
        key = rsa.PublicKey(rsaPublickey, 65537)
        message = str(self.jsonData['servertime']) + '\t' +str(self.jsonData['nonce']) + '\n' + str(self.userPasswd)  
        passwd = rsa.encrypt(message, key) 
        passwd = binascii.b2a_hex(passwd) 
        return passwd  

    def getUsername(self):
        username_ = urllib.quote(self.userName) 
        username = base64.encodestring(username_)[:-1] 
        return username 

    def getFormData(self):  
        userName = self.getUsername()  
        password = self.getPassword()  
        postData = {  
            'entry':'weibo',  
            'gateway':'1',  
            'from':'',  
            'savestate':'7',  
            'useticket':'1',  
            'pagerefer':'',  
            'pcid': '',  
            'door': '',
            'vsnf':'1',  
            'su':userName,  
            'service':'miniblog',  
            'servertime':str(self.jsonData['servertime']),  
            'nonce':str(self.jsonData['nonce']),  
            'pwencode':'rsa2',  
            'rsakv':str(self.jsonData['rsakv']),  
            'sp':password,  
            'sr':'1920*1080',  
            'encoding':'UTF-8',
            'cdult':'2',
            'domain':'weibo.com',
            'prelt':'115',  
            'url':'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',  
            'returntype':'META'  
        }  
        return  postData 
    def verifyCode(self):
        url = 'http://login.sina.com.cn/cgi/pin.php?r={randint}&s=0&p={pcid}'.format(  
            randint=int(random.random() * 1e8), pcid=self.jsonData['pcid'])  
        filename = 'pin.png'  
        if os.path.isfile(filename):  
            os.remove(filename)  
   
        urllib.urlretrieve(url, filename)  
        if os.path.isfile(filename):  # get verify code successfully      
            code = raw_input('请输入验证码:')  
            return dict(pcid=self.jsonData['pcid'], door=code)  
        else:  
            return dict() 
   
    def login(self, loginUrl):   
            postData = self.getFormData() 
            urlPattern = re.compile('location.replace\([\"\']([^\)]+)[\"\']\)')
            reUrlPattern = re.compile(r'feedBackUrlCallBack\(([^\)]+)\)')

            headers = self.headers  
            while not self.success:
                #print postData
                formData = urllib.urlencode(postData) 
                request  = urllib2.Request(  
                        url = loginUrl,  
                        data = formData,  
                        headers = headers  
                )  
                print 'open read'
                response = self.opener.open(request)  
                content = response.read()
                print 'open ok---->'
                #print content.decode('GB2312')
                try:
                    dirtyUrl = urlPattern.search(content)
                    url = dirtyUrl.group(1)
                    query = urlparse.parse_qs(urlparse.urlparse(url).query)
                    retcode = query['retcode'][0] 
                    if retcode != '0':
                        print query['reason'][0].decode('gbk')
                        print config.FAILCODE[retcode]
                        if  retcode == config.DISPLAY or retcode == config.NOTRIGHT:
                            postData.update(self.verifyCode())
                            continue
                        else :
                            return False
                    loginUrl = dirtyUrl.group(1) 
                    html = self.opener.open(loginUrl).read()
                    content = reUrlPattern.search(html) 
                    if not content :
                        print 'reurl info error login error'
                        return False
                    feedBack = content.group(1)
                    feedBack.replace('true', 'True').replace('null', 'None')
                    jsonData = json.loads(feedBack)
                    if not jsonData :
                        print 'error json loin error'
                        return False

                    self.success = jsonData['result']
                    self.userDomain = jsonData['userinfo']['userdomain'] 
                    print self.userDomain
                    if self.success:
                        print "Login success!"
                        break
                    else :
                        print 'unkonwn error' 
                        continue 
                except Exception as e:  
                    print e
                    print 'Login error!'  
                    return False  

            self.uniqueid = jsonData['userinfo']['uniqueid']
            mainUrl = 'http://weibo.com' + '/u/' + jsonData['userinfo']['uniqueid'] + '/home' + self.userDomain 
            request = urllib2.Request(mainUrl)  
            response = self.opener.open(request)  
            text = response.read() 
            ofile = open("index.html","w+")  
            ofile.write(text)  
            ofile.close() 
            return True
    def constrcutSession(self):
        session = Session(self.headers,self.userDomain,self.uniqueid,self.opener)
        return session
    def getCount(self,strcount):
        num = 0.0
        if u'亿' in strcount :
            index = strcount.find(u'亿')
            num =  float(strcount[0:index])
            num = num * 100000000
        elif u'万' in strcount:
            index = strcount.find(u'万')
            num =  float(strcount[0:index])
            num =  num * 10000
        else :
            num =  float( strcount)  
        return num  
    def gethotTheme(self):
        f = open('index.html')
        items = []
        content = f.read()
        content = content.replace('\/','/').replace('\\n','\n').replace('\\r','\r').replace('\\t','\t')
        Pattern = re.compile('FM.view\(\{([^\}]+)\}\)')
        soup = BeautifulSoup(content,'html.parser')
        elements = soup.find_all('script')
        for ele in elements:
            text = Pattern.search(ele.get_text())
            if text :
                FM = text.group(1)
                #pat = '''"domid":"Pl_Core_T8CustomTriColumn__3"'''
                pat = '''"v6_pl_rightmod_recominfo"'''
                if pat  in FM :
                    index = FM.find('html')
                    html = FM[index+6:len(FM)-1]
                    soup = BeautifulSoup(html,'html.parser')
                    rs = soup.find_all('li')
                    for r in rs:
                        item = Item()
                        url = r.a['href']
                        item.url = url[2:len(url)-2]
                        item.count = self.getCount(r.get_text().split('\n')[2])
                        item.theme = r.get_text().split('\n')[3].encode('UTF8')
                        items.append(item)
                        sorted(items, key=lambda Item: Item.count)
        return items

#sina.sendMessge('hello')
