# -*- coding: utf-8 -*-
class WeiboItem :
    def __init__(self,mid,date = '0',time = '0',itype = 'null',text = 'null',link = ''):
	self.mid = mid
	self.date = date
	self.itype = itype
	self.text = text
	self.link = link
	self.time = time
    def printInfo(self):
	print 'date:',self.date,'time:',self.time,'type:', self.itype,'text:',self.text,'link:',self.link,
	



