# -!- coding: utf-8 -!-
import time
import copy


def lrcremoveinfo(lrc):
    lines = lrc.split('\n')
    if lines[-1] == '':
        afterlines = copy.deepcopy(lines)[:-1]
    else:
        afterlines = copy.deepcopy(lines)
    offs = 0
    for i in range(len(afterlines)):  #忽略所有ID标签
        try:
            int(lines[i].split(':')[0][1:])
        except ValueError:
            del afterlines[i - offs]
            offs +=1
    return afterlines


def lrctimeconverter(lrc):
    orderedlrclist = []
    for i in range(len(lrc)):
        a = lrc[i].split(']')
        b = a[0].strip('[')
        d = b.index('.')
        c = b[d:]
        b = '1970 ' + b[:d]
        timearray = list((time.strptime(b, "%Y %M:%S")))
        timearray[3] += int(timearray[3] + int((time.strftime("%z", time.gmtime())[:3])))
        timestamp = time.mktime(tuple(timearray))
        orderedlrclist.append([timestamp + float(c), a[1]])
    return orderedlrclist


def listlrc(lrc):
    return lrctimeconverter(lrcremoveinfo(lrc))
