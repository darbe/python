#import json
class Session:
    def __init__ (self,headers=None, userDomain='',uniqueid='',opener=None):
        self.headers = headers
        self.userDomain = userDomain
        self.uniqueid = uniqueid
        self.opener = opener

#s = '''{"code":"100001","msg":"\u5fae\u535a\u53d1\u7684\u592a\u591a\u5566\uff0c\u4f11\u606f\u4e00\u4f1a\u518d\u53d1\u5566\uff01","data":{}}'''
#jsonData = json.loads(s)
#print jsonData['msg']