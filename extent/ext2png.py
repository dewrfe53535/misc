import clr
import struct
from PIL import Image
import sys
import io
import os
clr.AddReference("System.Drawing")
clr.AddReference("System")
clr.AddReference("Scarlet")
from Scarlet.Drawing import ImageBinary, PixelDataFormat
from System.Drawing.Imaging import ImageFormat
from System.IO import MemoryStream


def indexed8(fileobj, width, height):  # 08 00 00 00
    imageobj = ImageBinary()
    imageobj.Width = width
    imageobj.Height = height
    imageobj.InputPaletteFormat = PixelDataFormat.FormatArgb8888
    imageobj.InputEndianness = 0
    imageobj.InputPixelFormat = PixelDataFormat.FormatIndexed8
    filepalette = bytearray(fileobj.read(1024))
    fileimgdata = bytearray(fileobj.read())
    imageobj.AddInputPalette(filepalette)
    imageobj.AddInputPixels(fileimgdata)
    b = imageobj.GetBitmap(0, 0)
    bytebit = MemoryStream()
    b.Save(bytebit, ImageFormat.Png)
    b.Dispose()
    nimg = bytes(bytebit.GetBuffer())
    image = Image.open(io.BytesIO(nimg))
    bytebit.Dispose()
    return image


def bgra8(fileobj, width, height):  # 20 00 00 00
    decimg = Image.new('RGBA', (width + 1, height + 1))
    nowpixelw = 1
    nowpixelh = 1
    while True:
        co1 = fileobj.read(1)
        if co1 == b'':
            break
        co1 = int(co1.hex(), 16)
        co2 = int(fileobj.read(1).hex(), 16)
        co3 = int(fileobj.read(1).hex(), 16)
        co4 = int(fileobj.read(1).hex(), 16)
        decimg.putpixel((nowpixelw, nowpixelh), (co3, co2, co1, co4))  # BGRA->RGBA
        if nowpixelw == width:
            nowpixelh += 1
            nowpixelw = 1
        else:
            nowpixelw += 1
    return decimg


def parseheader(fileobj):
    header = fileobj.read(4).decode()
    assert header == 'EXT0'
    var4h_bh = fileobj.read(8)  # unknown
    width = struct.unpack('i', fileobj.read(4))[0]
    height = struct.unpack('i', fileobj.read(4))[0]
    width2 = struct.unpack('i', fileobj.read(4))[0]
    height2 = struct.unpack('i', fileobj.read(4))[0]
    pixformat2 = fileobj.read(4)  # if not F1 D8 FF FF ,it's pixel format?
    var20h_var23h = fileobj.read(4)  # usually F1 D8 FF FF or 00000000?
    pixformat = fileobj.read(4)  # pixel format
    var28h_var3fh = fileobj.read(24)  # unkown

    return header, width, height, width2, height2, pixformat2, pixformat


def main(filename):
    fileobj = open(filename, 'rb')
    header = parseheader(fileobj)
    pixformat, pixformat2, width, height = header[6], header[5], header[1], header[2]
    if pixformat2 == b'\x08\x00\x00\x00' or pixformat == b'\x08\x00\x00\x00':
        image = indexed8(fileobj, width, height)
    elif pixformat2 == b'\x20\x00\x00\x00' or pixformat == b'\x20\x00\x00\x00':
        image = bgra8(fileobj, width, height)
    else:
        exit("unsupported file type")
    image.save("%s.png" % os.path.basename(filename[:-4]))


if __name__ == '__main__':
    main(sys.argv[1])
