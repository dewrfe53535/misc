import requests
import urllib3
import re
import time
import json
from requests.adapters import HTTPAdapter
urllib3.disable_warnings()#便于fiddler调试


err_list = {0:'签到成功',
            '-100':'已签到过',
            '-101':'账号凭证已过期',
            '-102':'服务器端故障',}
class sign:

    def __init__(self):
        self.req = requests.session()#为了自动重试
        self.req.mount('http://',HTTPAdapter(max_retries=5))
        self.req.mount('https://',HTTPAdapter(max_retries=5))
        self.common_header = {'Connection': 'keep-alive',
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.16 Safari/537.36',
                         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                         'Accept-Language': 'zh-CN,zh;'
                         }
        self.req.headers.update(self.common_header)

    def afterreq(self):#便于下次请求
        self.req.headers.clear()
        self.req.headers.update(self.common_header)

    def diz_task_all(self,cookie,host,tid,https=False):
        if https == True:
            statusurl = 'https'
        else:
            statusurl = 'http'
        url1 = statusurl + '://%s/home.php?mod=task&do=apply&id=%s'%(host,tid)
        url2 = statusurl +'://%s/home.php?mod=task&do=draw&id=%s'%(host,tid)
        aheader = {'Referer':'https://%s/'%host,
                   'Cookie':cookie}
        self.req.headers.update(aheader)
        v1 = self.req.get(url1,timeout=15,verify=False, allow_redirects=False).text
        if '您已申请过'  in v1:
            self.afterreq()
            return '-100'
        elif '需要先登录' in v1:
            self.afterreq()
            return  '-101'
        self.req.headers.update(aheader)
        self.req.get(url2, timeout=15, verify=False)
        self.afterreq()
        return 0

    def diz_plugin_all(self,cookie,host,types,https=False):
        if https == True:
            statusurl = 'https'
        else:
            statusurl = 'http'
        url1 = statusurl + '://%s/plugin.php?id=dsu_paulsign:sign'%host
        url2 = statusurl + '://%s/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1'%host
        aheader = {'Referer':'https://%s/'%host,
                   'Cookie':cookie}
        self.req.headers.update(aheader)
        v1 = self.req.get(url1, timeout=15, verify=False).text
        try:
            formhash = re.findall(r'type="hidden" name="formhash" value="(.*?)"',v1)[0]
        except IndexError:
            self.afterreq()
            return '-100'
        if '密码' in v1:
            self.afterreq()
            return '-101'
        self.afterreq()
        postdata = 'formhash=%s&qdxq=%s&qdmode=3&todaysay=&fastreply=0'%(formhash,types)
        self.req.headers['content-type'] = 'application/x-www-form-urlencoded'
        self.req.headers.update(aheader)
        v2 = self.req.post(url2,data=postdata, timeout=15, verify=False).text
        self.afterreq()
        if '明天' in v2:
            return '-100'
        elif '负载' in v2:
            return '-102'
        return 0

    def jixiang_sign(self,token,memberid):#有问题，签到成功无法获取积分，待修
        url3 = 'https://app.maxxipoint.com/api/checkin/getTasks'
        postdata3 = r'{"bizContent":"{\"cityName\":\"%s\",\"memberGrade\":\"0\",\"memberId\":\"1133267001\"}","devContent":"{\"appIdentify\":\"com.maxxipoint.android\",\"appVersion\":\"5.5.1\",\"deviceModel\":\"Mi Max 2\",\"deviceVersion\":\"Mi Max 2-28-9\",\"deviceId\":\"531e5941-e19f-3072-81b5-c3502a2344f0\",\"platform\":\"android\"}"}'%memberid
        url2 = 'https://app.maxxipoint.com/api/checkin/initCheckinInfo'
        postdata2 = r'{"bizContent":"{\"memberId\":\"%s\"}","devContent":"{\"appIdentify\":\"com.maxxipoint.android\",\"appVersion\":\"5.5.1\",\"deviceModel\":\"Mi Max 2\",\"deviceVersion\":\"Mi Max 2-28-9\",\"deviceId\":\"531e5941-e19f-3072-81b5-c3502a2344f0\",\"platform\":\"android\"}"}'%memberid
        url1 = 'https://app.maxxipoint.com/api/checkin/doCheckin'
        postdata = r'{"bizContent":"{\"checkinId\":\"1\",\"memberId\":\"'+memberid+r'\"}","devContent":"{\"appIdentify\":\"com.maxxipoint.android\",\"appVersion\":\"5.4.6\",\"deviceModel\":\"Mi Max 2\",\"deviceVersion\":\"Mi Max 2-28-9\",\"deviceId\":\"531e5941-e19f-3072-81b5-c3502a2344f0\",\"platform\":\"android\"}"}'
        aheader = {'requestId':'531e5941-e19f-3072-81b5-c3502a2344f0',
                   'appId':'APPKHFJJ78897FH',
                   'reqType':'app',
                   'tokenId':token,
                   'timestamp':str(int(time.time()*1000)),
                   'Content-Type':'application/json;charset=utf-8'}
        self.req.headers.update(aheader)
        self.req.post(url3, data=postdata3, timeout=15, verify=False)
        self.req.post(url2,data=postdata2, timeout=15, verify=False)
        v1 = self.req.post(url1, data=postdata, timeout=15, verify=False).json()['data']
        v1 = json.loads(v1)['respCode']
        self.afterreq()
        if v1 == '00':
            return 0
        elif v1 == 'A0':
            return '-100'
        else:
            return '-101'

    def ssr_panel_sign(self,cookie,host,https=False):
        if https == True:
            statusurl = 'https'
        else:
            statusurl = 'http'
        url1 = statusurl +'://%s/user/checkin'%host
        aheader = {'Referer':'https://%s/'%host,
                           'Cookie':cookie}
        self.req.headers.update(aheader)
        v1 = self.req.post(url1, timeout=15, verify=False).text
        self.afterreq()
        if '\\u83b7\\u5f97\\u4e86' in v1:
            return 0
        elif 'u7b7e\\u5230\\u8fc7\\u4e86' in v1:
            return '-100'
        return '-101'

    def just_get(self,url,cookie,username,header=None):
        if header != None:
            self.req.headers.update(header)
        aheader = {'Cookie':cookie}
        self.req.headers.update(aheader)
        v1 = self.req.get(url, timeout=15, verify=False).text
        self.afterreq()
        if username in v1:
            return 0
        return '-101'

    def phpwind1(self,host,cookie,verfiycode,user_age,https=False):#有UA校验
        if https == True:
            statusurl = 'https'
        else:
            statusurl = 'http'
        url1 = statusurl+'://'+host+'/jobcenter.php?action=punch&verify={0}&nowtime={1}&verify={0}'.format(verfiycode,int(time.time()*1000))
        aheader = {'Cookie':cookie}
        self.req.headers.update(aheader)
        self.req.headers['User-Agent'] = user_age
        self.req.headers['content-type'] = 'application/x-www-form-urlencoded'
        data = 'step=2'
        v1 = self.req.post(url1,data=data, timeout=15, verify=False).text
        self.afterreq()
        if r'flag":' in v1:
            return 0
        else:
            return -100