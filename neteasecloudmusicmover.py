# 网易云api基于   https://github.com/Binaryify/NeteaseCloudMusicApi
import requests
import re
import time

bgm_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36'
bgm_cookie = ''
bgm_gh = 'f2d8ca90'
playlistid = '377736457'  # 网易云 playlistid
sstartnum =  None # 开始添加的歌曲的位置
sendnum = None  # 结束的歌曲的位置
bgm_index_id =25646


def convertbrowsercookiesdict(s):
    '''Covert cookies string from browser to a dict'''
    ss = s.split(';')
    outdict = {}
    for item in ss:
        i1 = item.split('=', 1)[0].strip()
        i2 = item.split('=', 1)[1].strip()
        outdict[i1] = i2
    return outdict


bgm_cookie_cvd = convertbrowsercookiesdict(bgm_cookie)


def removesymbol(line):  # 避免因符号中英问题无法搜索出
    string1 = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+—()?【】「」 “”・！，。？、~@#￥%…&*（）]+|TVアニメ|PCゲーム", " ", line)
    return string1


songlist = []
playlist = requests.get('http://127.0.0.1:3000/playlist/detail?id=%s' % playlistid).json()
for i in playlist['playlist']['tracks']:
    songlist.append([removesymbol(i['name']), removesymbol(i['al']['name'])])  # 转换songlist

bgm_search_api = 'http://api.bgm.tv/search/subject/%s?type=3'
bgm_done_url = 'http://bgm.tv/subject/%s/interest/update?gh=' + bgm_gh
bgm_done_post = 'referer=ajax&interest=2&tags=&comment=&update=%E4%BF%9D%E5%AD%98'
bgm_index_url = 'http://bgm.tv/index/%s/add_related'
bgm_index_post = 'formhash=%s&cat=3&add_related=%s&submit=添加章节关联'
unknown = ''
bgmreq = requests.session()
for i in songlist[sstartnum:sendnum]:
    continuecontrol = 0
    while True:
        try:
            a = bgmreq.get(bgm_search_api % i[1], cookies=bgm_cookie_cvd, headers={'user-agent': bgm_user_agent}).json()
        except:
            time.sleep(1)
        try:
            if str(a['code']) == "404":
                unknown += str(i) + '\n'
                print("%s 未找到" % i[0])
                continuecontrol = 1
        except:
            try:
                b = a['list'][0]['id']
            except:
                print("无法获取list")  # 极少情况下会出现list为空的情况
                unknown += str(i) + '\n'
                continuecontrol = 1
        break
    if continuecontrol == 1:
        continue
    bgm_name = a['list'][0]['name']
    urlbgm = 'http://bgm.tv/subject/' + str(b) + '/ep'
    c = requests.get(urlbgm, cookies=bgm_cookie_cvd, headers={'user-agent': bgm_user_agent})
    c.encoding = 'utf-8'  # 指定解码，不能自动识别也是很迷。。。
    c = c.text
    regex1 = re.compile(r'"line_detail">([\s\S]*)<input class="inputBtn" value="批量修')
    d = re.findall(regex1, c)  # 缩小范围(并没有好好学正则
    e = d[0]
    regex3 = re.compile(r'value="(.*?)"')
    regex4 = re.compile(r">(.*?)</a></h6>")  # 提取歌曲与id
    bgm_sid = re.findall(regex3, e)
    bgm_sname = re.findall(regex4, e)
    for index, j in enumerate(bgm_sname):  # 找出对应歌曲的在列表中的下标
        if i[0] in removesymbol(j):
            prereq = bgm_sid[index]
            break
    try:
        bgmreq.post(bgm_index_url % bgm_index_id, data=(bgm_index_post % (bgm_gh, prereq)).encode("utf-8"),
                    cookies=bgm_cookie_cvd,
                    headers={'user-agent': bgm_user_agent, 'Content-Type': 'application/x-www-form-urlencoded'})
        bgmreq.post(bgm_done_url % b, data=bgm_done_post, cookies=bgm_cookie_cvd,
                    headers={'user-agent': bgm_user_agent})
        del prereq
    except:
        unknown += str(i)
print(unknown)
