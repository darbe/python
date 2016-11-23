# -*- coding: utf-8 -*-
PRELOGINURL = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=emhhbmd3dXpoYW8lNDBzaW5hLmNu&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_=1476364797049'
LOGINURL = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
FAILCODE =  { 
                '-1': '登录成功',
                '0': '登录系统错误，请稍后尝试',
                '1': '您的用户名和密码不匹配',
                '2': '您的用户名和密码不匹配',
                '4': '您的用户名和密码不匹配',
                '4040': '登录次数过多',
                '2070': '输入的验证码不正确',
                '2093': '抱歉！登录失败，请稍候再试',
                '6102': '请输入密码和账号',
                '101': '登录名或密码错误',
                '4049': '为了您的帐号安全，请输入验证码',
                '4038': '登录次数过多'
            }
DISPLAY = '4049'
NOTRIGHT = '2070'
ERRORCODE = -1
#USRNAME = 'zhangwuzhao@sina.cn'
#PASSWD = '530698376abc'
USRNAME = 'lantuling@126.com'
PASSWD = '530698376'
SENDSUCC = '100000'
