# 存放一些杂七杂八的有关bili的东西

import biliinit
import time


def delfav():  # 清空B站默认收藏夹
    api1 = 'https://app.bilibili.com/x/v2/favorite/video'
    access = ''
    api2 = 'https://api.bilibili.com/x/v2/fav/video/del'  # mdel操作过于频繁，还不如遍历然后del写起来简单...
    fid = 1946150
    bilir = biliinit.bilireq(access)
    page = 1
    data = []
    while True:
        t1 = bilir.req(api1, getdata=[('vmid', 841451), ('fid', fid), ('ps', 999), ('pn', page), ('order', 'ftime')],
                       reqtype=1).json()['data']['items']
        if not t1:
            break
        for i in t1:
            data.append(i['aid'])
        page += 1
    for i in data:
        bilir.req(api2, postdata=[('aid', i)], reqtype=1)
        time.sleep(1)  # 503：调用速度过快 (╯‵□′)╯︵┻━┻


def mvfo():  # 移动bili关注
    acc1 = ''
    acc2 = ''
    # a账号1 -> 账号2
    api1 = 'https://api.bilibili.com/x/relation/tag'
    api2 = 'https://api.bilibili.com/x/relation/modify'
    tagid = '18897'  # 分组

    a1 = biliinit.bilireq()
    a1.access = acc1
    a2 = biliinit.bilireq()
    a2.access = acc2

    page = 1
    data = []
    while True:
        t1 = a1.req(api1, getdata=[('ps', 999), ('pn', page), ('tagid', tagid)], reqtype=1).json()['data']  # 取关注列表
        if not t1:
            break
        for i in t1:  # 遍历,获取关注mid列表
            data.append(i['mid'])
        page += 1
    for i in data:  # 转移
        a1.req(api2, postdata=[('act', 2), ('re_src', 34), ('fid', i)], reqtype=1)
        a2.req(api2, postdata=[('act', 1), ('re_src', 34), ('fid', i)], reqtype=1)


def unfollowbangumi():  # 取消订阅所有番剧
    a1 = biliinit.bilireq()
    a1.login_by_pass('', '')
    api1 = 'https://bangumi.bilibili.com/follow/web_api/season/unfollow'
    api2 = 'http://space.bilibili.com/ajax/Bangumi/getList?mid=%s&page=%s'
    npage = a1.req(api2 % (a1.uid, 1)).json()['data']['pages']
    seaid = []
    for i in range(1, npage + 1):
        data = a1.req(api2 % (a1.uid, i)).json()['data']['result']
        for j in data:
            seaid.append(j['season_id'])
    for i in seaid:
        a1.req(api1, postdata=[('season_id', i), ('season_type', 1)], reqtype=2)


a1 = biliinit.bilireq()
a1.login_by_cookies('DedeUserID=841451;DedeUserID__ckMd5=66f8d536d5f459fd;SESSDATA=9e97a8f4%2C1533323064%2C3357c817;bili_jct=58463fc33e0107a6e5e404e308f6b854;sid=4zfxv9n6')
print(a1.cookies)