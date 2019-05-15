import json

#TODO:有时间学了xml结构后大概会重写(

xml_head = '<?xml version="1.0" encoding="UTF-8"?><i><chatserver>chat.bilibili.com</chatserver><chatid>31555858</chatid><mission>0</mission><maxlimit>3000</maxlimit><state>0</state><real_name>0</real_name><source>k-v</source>'
xml_body = '<d p="%s,%s,%s,%s,0,0,%s,%s">%s</d>'#https://zhidao.baidu.com/question/1430448163912263499.html
xml_end = '</i>'
filename = ''

def xmlreplace(stri):#xml转义
    stri = stri.replace('<','&lt;')
    stri = stri.replace('>', '&gt;')
    stri = stri.replace('&', '&amp;')
    stri = stri.replace("'", '&apos;')
    stri = stri.replace('"', '&quot;')
    return stri

with open(filename,encoding='utf-8') as f:
    json_data = json.load(f)

nf = open(filename+'.xml',"a+",encoding="utf-8")
nf.write(xml_head)
for i in json_data:
    time = i['time']
    if i['position']==0:
        mode = 1
    elif i['position']==2:
        mode = 4
    else:
        mode = 5
    if i ['size'] ==0:
        bsize = 18
    elif i['size']==2:
        bsize = 36
    else:
        bsize = 25
    color = int(i['color'].strip("#"), 16)
    nf.write(xml_body%(time/10,mode,bsize,color,i['userid'],i['sn'],xmlreplace(i['text'])))
nf.write(xml_end)
nf.close()