from ext2png import *
import os
import sys, getopt


def parsearc(fileobj, strcode='cp932'):
    header = fileobj.read(4)
    filecount = struct.unpack('l', fileobj.read(4))[0]
    objlist = []
    for i in range(filecount):
        filename = fileobj.read(64).decode(strcode, errors="ignore").strip('\uf8f2').strip('\x00')
        filelength = struct.unpack('l', fileobj.read(4))[0]
        fileoffset = struct.unpack('l', fileobj.read(4))[0]
        objlist.append((filename, filelength, fileoffset))
    return objlist, filecount


def extractarc(fileobj, fileloc):

    filename2 = os.path.basename(fileloc[:-4])
    filename = os.path.basename(fileloc)
    if not os.path.exists(filename2):
        os.mkdir(filename2)
    fileinfo = parsearc(open(fileloc, "rb"))
    filelist = fileinfo[0]
    for i in filelist:
        with open('.\\%s\\' % filename2 + i[0], 'wb') as f:
            fileobj.seek(i[2])
            f.write(fileobj.read(i[1]))


def parsebin(fileobj):
    iwidth = struct.unpack('l', fileobj.read(4))[0]
    iheight = struct.unpack('l', fileobj.read(4))[0]
    count = struct.unpack('l', fileobj.read(4))[0]
    assert fileobj.read(4) == b'\xcc\xcc\xcc\xcc'  # imagefiledata
    imageinfo = []
    for i in range(count):
        posx = struct.unpack('l', fileobj.read(4))[0]
        posy = struct.unpack('l', fileobj.read(4))[0]
        width = struct.unpack('l', fileobj.read(4))[0]
        height = struct.unpack('l', fileobj.read(4))[0]
        imageinfo.append((posx, posy, width, height))
    return imageinfo, iwidth, iheight


def convertimagefromMemory(fileobj, fileloc):
    fileobj2 = fileobj
    arcinfo = parsearc(fileobj2)[0]
    for i in arcinfo:
        if i[0] == 'info.bin':
            fileobj2.seek(i[2])
            bininfo = parsebin(fileobj2)
    try:
        bininfo ==''
    except:
        exit("this file may not a single image file")
    imgfile = Image.new('RGBA', (bininfo[1], bininfo[2]))
    for i in range(len(bininfo[0])):
        fileobj.seek(arcinfo[i][2])
        filedata = io.BytesIO(fileobj.read(arcinfo[i][1]))

        boxdata = (bininfo[0][i][0], bininfo[0][i][1])
        header = parseheader(filedata)
        pixformat, pixformat2, width, height = header[6], header[5], header[1], header[2]
        if pixformat2 == b'\x08\x00\x00\x00' or pixformat == b'\x08\x00\x00\x00':
            image = indexed8(filedata, width, height)
        elif pixformat2 == b'\x20\x00\x00\x00' or pixformat == b'\x20\x00\x00\x00':
            image = bgra8(filedata, width, height)
        newimage = image.convert('RGBA')
        imgfile.paste(newimage, box=boxdata)
    imgfile.save("%s.png" % os.path.basename(fileloc[:-4]))


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "e:c:")
        assert argv != []
    except :
        print('''
        arc2png.py [-e <inputfile>] [-c <iutputfile>]
        -e convert .arc to .png
        -c extract .arc in cp932
        ''')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-e"):
            extractarc(open(arg, "rb"), arg)
        elif opt in ("-c"):
            convertimagefromMemory(open(arg, "rb"),arg)
if __name__ == '__main__':
    main(sys.argv[1:])