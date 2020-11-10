#!/usr/bin/python
# -*- coding: UTF-8 -*-

# For view figures in termial. by Jian Liu PhD.

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from PIL import Image,ImageFilter

COLS, LINES = 80, 60 # LINES must be an even number

def printl(id1, id2):
    """print two half blocks, ANSI color. id1=upper, id2=lower"""
    sys.stdout.write(u"\u001b[48;5;%d;38;5;%dm\u2584"%(id1,id2))

def printc(id1, id2):
    """print two half blocks, 24bit. id1=upper, id2=lower"""
    sys.stdout.write(u"\u001b[48;2;%d;%d;%d;38;2;%d;%d;%dm\u2584"\
                      %(id1[0],id1[1],id1[2],id2[0],id2[1],id2[2]))

def printa(id1):
    '''print a ascii char'''
    char_list = "#X%x+:. " # length-8
    sys.stdout.write(char_list[id1/(256/len(char_list))])

def println():
    """print new line and reset the color"""
    print u"\u001b[0m"

def viewer(imgfile, mode="24bit"):
    im = Image.open(imgfile)

    im_size = im.getbbox()
    im_width, im_height = im_size[2]-im_size[0], im_size[3]-im_size[1]
    if 1.0*im_width/im_height > 1.0*COLS/LINES:
        im_height = 2*int(0.5*im_height*COLS/im_width) 
        im_width = COLS
    else:
        im_width = int(1.0*im_width*LINES/im_height)
        im_height = LINES 

    if mode == "24bit":
        im = im.resize((im_width, im_height), Image.ANTIALIAS)
        im = im.filter(ImageFilter.GaussianBlur(radius=0.5))  
        im_data = im.getdata()
        for i in range(0, im_height, 2):
            for j in range(0, im_width):
                colorid1 = im_data[  i  *im_width + j]
                colorid2 = im_data[(i+1)*im_width + j]
                printc(colorid1, colorid2)
            println()
    elif mode == "gray":
        im = im.resize((im_width, im_height), Image.ANTIALIAS)
        im = im.convert('L')
        im = im.filter(ImageFilter.GaussianBlur(radius=0.5))  
        im_data = im.getdata()
        for i in range(0, im_height, 2):
            for j in range(0, im_width):
                colorid1 = im_data[  i  *im_width + j]/10+232
                colorid1 = colorid1 if colorid1 < 256 else 15
                colorid2 = im_data[(i+1)*im_width + j]/10+232
                colorid2 = colorid2 if colorid2 < 256 else 15
                printl(colorid1, colorid2)
            println()
    elif mode == "ascii":
        im = im.resize((im_width, im_height), Image.ANTIALIAS)
        im = im.convert('L')
        im = im.filter(ImageFilter.GaussianBlur(radius=0.5))
        im_data = im.getdata()
        for i in range(0, im_height, 2):
            for j in range(0, im_width):
                colorid = (im_data[i*im_width+j]+im_data[(i+1)*im_width+j])/2
                printa(colorid)
            println()
    elif mode == "blackwhite":
        im = im.resize((im_width, im_height), Image.ANTIALIAS)
        im = im.convert('1')
        im_data = im.getdata()
        for i in range(0, im_height, 2):
            for j in range(0, im_width):
                colorid1 = 0 if im_data[  i  *im_width + j] == 0 else 15
                colorid2 = 0 if im_data[(i+1)*im_width + j] == 0 else 15
                printl(colorid1, colorid2)
            println()
    else:
        print "Error: I don't konw " + mode + "mode"
        return 0

if __name__ == '__main__':
    modes = {'-a':'ascii', '-b':'blackwhite', '-c':'24bit', '-g':'gray'}
    if len(sys.argv) == 2:
        imgfile = sys.argv[1]
        viewer(imgfile, "24bit")
    elif len(sys.argv) == 3 and sys.argv[1] in modes:
        imgfile = sys.argv[2]
        viewer(imgfile, modes[sys.argv[1]])
    else:
        print "Usage: %s -<abcg> imagefile" % sys.argv[0]
