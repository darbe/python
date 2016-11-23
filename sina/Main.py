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
    forword = forwardMsger(session)
    forword.forwardMessge('forward ok--->','4044579365261598')
if False:
    session =  sina.constrcutSession()
    send = SendMsger(session)
    for item in items:
        send.sendMessge(item.theme+ ' '+ str(time.asctime()))
        break
        time.sleep(1)

if response:
    session =  sina.constrcutSession()
    send = SendMsger(session)
    send.sendMessge('this is ling ying chao',True,'f:\\zipai.jpg')

if False:
    
    session =  sina.constrcutSession()
    delete = DeleteMsger(session)
    delete.deleteAll()
    #sender = SendMsger(session)
    #for item in items:
    #    print item.theme
    #    time.sleep(1)
    #    sender.sendMessge(item.theme + '  ' ) 
    
