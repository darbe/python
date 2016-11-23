#encoding=utf8
import urllib2
import urllib
import BeautifulSoup
import socket

def getAllIps(proxyUrl):
    UserAgent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    header = {}
    header['User-Agent'] = UserAgent
    
    req = urllib2.Request(proxyUrl,headers=header)
    res = urllib2.urlopen(req).read()
    soup = BeautifulSoup.BeautifulSoup(res)
    ips = soup.findAll('tr')
    f = open("proxy","w")
    for x in range(1,len(ips)):
        ip = ips[x]
        tds = ip.findAll("td")
        ipTemp = tds[1].contents[0]+"\t"+tds[2].contents[0]+"\n"
        f.write(ipTemp)
    f.close()

def getVaildIps(targetUrl):
    socket.setdefaulttimeout(3)
    f = open("proxy")
    lines = f.readlines()
    proxys = []
    for i in range(0,len(lines)):
        ip = lines[i].strip("\n").split("\t")
        proxyHost = "http://"+ip[0]+":"+ip[1]
        proxyTemp = {"http":proxyHost}
        proxys.append(proxyTemp)
    f = open("sina","w")
    print len(proxys)
    for proxy in proxys:
        try:
            res = urllib.urlopen(targetUrl,proxies=proxy).read()
            ipPort = proxy['http']
            print ipPort
            f.write(ipPort+'\n')
        except Exception,e:
            print e
            continue
    f.close()


proxyUrl = 'http://www.xicidaili.com/nn/1'
targetUrl = "http://weibo.com/"
getAllIps(proxyUrl)
getVaildIps(targetUrl)