# -*- coding: utf-8 -*- 
from sina import SinaLogin
import config
from sendMsg import SendMsger
from forwardMsg import forwardMsger
from deleteMsg import DeleteMsger
import time
#from sendMsg import SendMsg
sina = SinaLogin(config.USRNAME,config.PASSWD)
response = sina.login(config.LOGINURL)
items = sina.gethotTheme()
print 'log ok'

if False:
    session =  sina.constrcutSession()
    forward = forwardMsger(session)
    forward.forwardMessge('forward ok--->','4044323747597688')
    print 'forward ok'
if False:
    session =  sina.constrcutSession()
    send = SendMsger(session)
    for i in range(10000):
        for item in items:
#            send.sendMessge(item.theme+ ' '+ str(time.asctime()))
            send.sendMessge(item.theme+ ' '+ u'互相关注吧 爱你哦')
            time.sleep(1)

if False:
    session =  sina.constrcutSession()
    send = SendMsger(session)
    #send.sendMessge('this is ling ying chao',True,'f:\\zipai.jpg')
    send.sendMessge('this is ling ying chao',True,'f:\\IMG_0073.PNG f:\\zipai.jpg f:\\IMG_0109.JPG')

if response:
    
    session =  sina.constrcutSession()
    delete = DeleteMsger(session)
    delete.deleteAll()
    #sender = SendMsger(session)
    #for item in items:
    #    print item.theme
    #    time.sleep(1)
    #    sender.sendMessge(item.theme + '  ' ) 
    
