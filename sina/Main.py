# -*- coding: utf-8 -*- 
from sina import SinaLogin
import config
from sendMsg import SendMsger
from forwardMsg import forwardMsger
from deleteMsg import DeleteMsger
import time
import logging
import log
logger = logging.getLogger("root")
#from sendMsg import SendMsg
logger.debug('<------------------creat login Class------------------>')
sina = SinaLogin(config.USRNAME,config.PASSWD)
 
logger.debug('<------------------start login ------------------>')
response = sina.login(config.LOGINURL)
logger.debug('<------------------login ok------------------>')
items = sina.gethotTheme()
logger.debug('<------------------get hot theme ok------------------>')
status = [0,0,0,1]
if status[0] and response:
    session =  sina.constrcutSession()
    forward = forwardMsger(session)
    forward.forwardMessge('forward ok--->','4044323747597688')
if status[1] and response:
    session =  sina.constrcutSession()
    send = SendMsger(session)
    for i in range(2):
        for item in items:
#            send.sendMessge(item.theme+ ' '+ str(time.asctime()))
            send.sendMessge(item.theme+ ' '+ u'互相关注吧 爱你哦')
            time.sleep(1)

if status[2] and response:
    session =  sina.constrcutSession()
    send = SendMsger(session)
    #send.sendMessge('this is ling ying chao',True,'f:\\zipai.jpg')
    send.sendMessge('this is ling ying chao',True,'f:\\IMG_0073.PNG f:\\zipai.jpg f:\\IMG_0109.JPG')

if status[3] and response:
    
    session =  sina.constrcutSession()
    delete = DeleteMsger(session)
    delete.deleteAll()
    #sender = SendMsger(session)
    #for item in items:
    #    print item.theme
    #    time.sleep(1)
    #    sender.sendMessge(item.theme + '  ' ) 
    
