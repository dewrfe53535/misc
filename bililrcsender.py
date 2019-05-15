# -!- coding: utf-8 -!-
# 网易云api基于   https://github.com/Binaryify/NeteaseCloudMusicApi
import lrcpaser
import requests
import random
from biliinit import bilireq
import time
import urllib.parse

def getlrcfromnetease(neteaselrcid,cl=1):# cl :是否中文
    lrclist = requests.get('http://127.0.0.1:3000/lyric?id=%s' % neteaselrcid).json()
    slrc = lrcpaser.listlrc(lrclist['lrc']['lyric'])
    try:
        clrc = lrcpaser.listlrc(lrclist['tlyric']['lyric'])
    except:
        print("无中文")
        cl = 0
    if cl == 1:
        plrc = clrc
    else:
        plrc = slrc
    return  plrc

def loadlocallrc(fileaddr):
    with open(fileaddr,'r',encoding='utf-8') as f:
        flrc = lrcpaser.listlrc(f.read())
        print(f.read())
    return  flrc

def send_danmaku(alllrc,offset,aid,cid,access,color=16777215,danstart =None,danend = None):
    input("请确认lrc:"%alllrc)
    bili = bilireq(access)
    for fortime, formsg in alllrc[danstart:danend]:
        if formsg == '':
            continue
        while True:
            a = bili.req(api='https://api.bilibili.com/x/v2/dm/post', getdata=[('aid', aid), ('oid', cid)],
                         postdata=[('pool', 0), ('rnd', int(time.time())),
                                   ('msg', urllib.parse.quote_plus(formsg, encoding='utf-8')), ('oid', cid),
                                   ('progress', int((fortime + offset) * 1000)), ('fontsize', 18), ('mode', '4'),
                                   ('color', color), ('plat', 2), ('screen_state', 0), ('from', 3), ('type', 1)],
                         reqtype=1)
            time.sleep(int(random.uniform(8, 15)))
            if str(a.json()['code']) == '0':
                break
            if str(a.json()['code']) == '36703':
                time.sleep(60)

def genBASdanmaku(lrclist,x,y,waittime = 5.0,dt = 4.0):
    lrcfirst = round(lrclist[1][0] - lrclist[0][0],3)
    with open('bas.txt','w+') as f:
        text1 = '''def text c {
    content = "%s"
    fontSize = 5%%
    x = %s%%
    y = %s%%
    anchorX = 0.5
    anchorY = 0.5
}
set c {} %ss
'''
        f.write(text1%(lrclist[0][1],x,y,lrcfirst))
        for i in range(1,len(lrclist)-1):
            if lrclist[i + 1][0] - lrclist[i][0] <waittime:
                lrctime = round(lrclist[i + 1][0] - lrclist[i][0],3)
                f.write('''then set c {
                    content = "%s"
                } %ss\n''' % (lrclist[i][1], lrctime))
            else:
                lrctime = dt
                f.write('''then set c {
                    content = "%s"
                } %ss\n''' % (lrclist[i][1], lrctime))
                f.write('''then set c {
                            content = ""
                        } %ss\n''' % (round(lrclist[i + 1][0] - lrclist[i][0]-dt,3))
                        )
        f.write('''then set c {
    content = "%s"
} %ss'''%(lrclist[len(lrclist)-1][1],5))
genBASdanmaku(loadlocallrc('C:/Users/dewrf/Documents/☆ぱ・ぴ・ぷ・ぺ・ぽりしー☆.lrc'),50,85,7,5)
