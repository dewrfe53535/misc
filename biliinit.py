import requests
import hashlib
import urllib3
import collections
import time
import rsa
import base64
import re
from urllib import parse

urllib3.disable_warnings()


class bilireq:
    def __init__(self):
        self.appkey = '84956560bc028eb7'
        self.appsec = '94aba54af9065f71de72f5508f1cd42e'
        self.platform = 'android'
        self.build = 523002
        self.requ = requests.session()
        self.access = ''
        self.cookies = ''
        self.csrf = ''
        self.uid = ''
        self.headers = collections.OrderedDict([('Content-Type', 'application/x-www-form-urlencoded; charset=utf-8'),
                                                ('Device-ID', 'QHQSJ0MhE3BHdRQnWydGcxF3EyscfT1PJxElSCpWNwJgBmJabQw')
                                                ])

    def sign(self, data, appsec=None):  # 签名,算法来自biliapi
        md5 = hashlib.md5()
        if appsec == None:
            appsec = self.appsec
        md5.update(bytes(data + appsec, encoding="utf-8"))
        return md5.hexdigest()

    def login_by_pass(self, user, password):
        # edit from :Dawnnnnnn/bilibili-tools/ no license provided
        url = 'https://passport.bilibili.com/api/oauth2/getKey'
        temp_params = 'appkey=1d8b6e7d45233436'
        sign = self.sign(temp_params, appsec='560c52ccd288fed045859ed18bffd973')
        params = {'appkey': '1d8b6e7d45233436', 'sign': sign}
        response = requests.post(url, data=params, verify=False)
        value = response.json()['data']
        key = value['key']
        Hash = str(value['hash'])
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(key.encode())
        password = base64.b64encode(rsa.encrypt((Hash + password).encode('utf-8'), pubkey))
        password = parse.quote_plus(password)
        url = "https://passport.bilibili.com/api/v2/oauth2/login"
        temp_params = 'appkey=1d8b6e7d45233436&password=' + password + '&username=' + user
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        payload = temp_params + "&sign=" + self.sign(temp_params, appsec='560c52ccd288fed045859ed18bffd973')
        response = requests.post(url, data=payload, headers=headers, verify=False)
        try:
            cookie = (response.json()['data']['cookie_info']['cookies'])
            cookie_format = ""
            for i in range(0, len(cookie)):
                cookie_format = cookie_format + cookie[i]['name'] + "=" + cookie[i]['value'] + ";"
            s1 = re.findall(r'bili_jct=(\S+)', cookie_format, re.M)
            s2 = re.findall(r'DedeUserID=(\S+)', cookie_format, re.M)
            self.cookies = cookie_format
            self.headers['Cookie'] = self.cookies
            self.csrf = (s1[0]).split(";")[0]
            self.uid = (s2[0].split(";")[0])
            self.access = response.json()['data']['token_info']['access_token']
            print('login succeed')
        except:
            print("failed:", response.json())

    def login_by_cookies(self, cookies):
        ss = cookies.split(';')
        outdict = {}
        self.cookies = cookies
        self.headers['Cookie'] = self.cookies
        for item in ss:
            i1 = item.split('=', 1)[0].strip()
            i2 = item.split('=', 1)[1].strip()
            outdict[i1] = i2
        try:
            self.csrf = outdict['bili_jct']
            self.uid = outdict['DedeUserID']
        except:
            print("failed:value not found")
        accurl = 'https://secure.bilibili.com/login?api=http%3A%2F%2Flink.acg.tv%2Fbilibili_connect.php%3Fmod%3Dauth%26op%3Dcallback&appkey=8907c61e930c789c&sign=4774633fd585a2477d9f329105d7f1e7'
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        }
        try:
            furl = requests.get(accurl, headers=headers, cookies=outdict, verify=False)
            purl = furl.url
            self.access = re.findall(r'access_key=(\S+)&m', purl)[0]
            print('login succeed')
        except:
            print('login failed,cookie is invalid')

    def login_by_access_key(self, access_key):
        url = 'https://passport.bilibili.com/api/login/sso?'
        tm_data = 'access_key=%s&appkey=1d8b6e7d45233436' % access_key
        sign = self.sign(tm_data, appsec='560c52ccd288fed045859ed18bffd973')
        rec = requests.get(url + tm_data + '&sign=' + sign, verify=False, allow_redirects=False)
        self.access = access_key
        browserstyle = ''
        try:
            for key, values in rec.cookies.get_dict().items():
                browserstyle += key + '=' + values + ';'
            self.cookies = browserstyle[:-1]
            self.uid = rec.cookies['DedeUserID']
            self.csrf = rec.cookies['bili_jct']
            print('login succeed')
        except:
            print('login failed,access_key is invalid')

    def req(self, api, postdata=None, getdata=None, reqtype=None, nosign=False):  # reqtype:0:None,1:android，2：PC
        param = ''
        paramget = ''
        parampost = ''
        apiurl = api
        postdatasign = False
        getdatasign = False
        if postdata != None and getdata != None:
            postdatasign = True
            getdatasign = True
        elif postdata != None:
            postdatasign = True
        elif getdata != None:
            getdatasign = True

        if reqtype == 1:
            getdata += [('appkey', self.appkey), ('access_key', self.access), ('platform', self.platform),
                        ('mobi_app', self.platform), ('ts', int(time.time()))]
        if reqtype == 2:
            postdata += [('csrf', self.csrf)]
        if getdatasign == True:
            getdata.sort()  # a-z排序
            for i, j in getdata:
                paramget += i + '=' + str(j) + '&'
            paramget = paramget[:-1]
            signstrget = self.sign(paramget)
            apiurl = api + paramget
            if nosign == False:
                apiurl += '&sign=' + signstrget
        if postdatasign == True:
            if getdatasign == False and reqtype == 1:
                postdata += [('appkey', self.appkey), ('access_key', self.access), ('platform', self.platform),
                             ('mobi_app', self.platform), ('ts', int(time.time()))]
            postdata.sort()
            for i, j in postdata:
                parampost += i + '=' + str(j) + '&'
            parampost = parampost[:-1]
            signstrpost = self.sign(parampost)
            apidata = parampost
            if nosign == False:
                apidata += '&sign=' + signstrpost
        if postdatasign == True:
            return self.requ.post(apiurl, data=apidata, headers=self.headers, verify=False)
        if postdatasign == False and getdatasign == True:
            return self.requ.get(apiurl, headers=self.headers, verify=False)
        return self.requ.get(apiurl, headers=self.headers, verify=False)
