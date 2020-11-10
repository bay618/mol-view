#!/usr/bin/env python
#-*- coding: UTF-8 -*-

# For render the molecular structues from xyz-file to image

import sys
import numpy as np
from itertools import combinations
from PIL import Image
from PIL import ImageDraw

# user defination
SIZE   = (300, 300) # size of the canves
MARGIN =  20

radius_dic = {'H':0.5, 'X':0.9} # in Ang
color_dic  = {'H' :'white',
              'Li':'blue',
              'C' :'cyan',
              'N' :'blue',
              'O' :'red',
              'F' :'green',
              'Na':'blue',
              'S' :'yellow',
              'Si':'yellow',
              'Cl':'green',
              'K' :'blue',
              'Cs':'blue',
              'Al':'purple',
              'Fe':'black',
              'Cu':'orange',
              'Au':'yellow',
              'Pt':'gray',
              'X' :'gray'}

# 
if len(sys.argv) == 2:
    view_ang = '-y'
    xyz_file = sys.argv[1]
elif len(sys.argv) == 3:
    view_ang = sys.argv[1]
    xyz_file = sys.argv[2]
else:
    print "Usage: %s <±x/y/z> xyz-file" % sys.argv[0]
    exit()

# load name and coord from xyz-file
xyz_data = open(xyz_file, "r").readlines()
atm_num  = int(xyz_data[0])
name     =             [i[0:-1].split()[0] for i in xyz_data[2:atm_num+2]]
xyz      = [map(float, [i[0:-1].split()[1] for i in xyz_data[2:atm_num+2]]),
            map(float, [i[0:-1].split()[2] for i in xyz_data[2:atm_num+2]]),
            map(float, [i[0:-1].split()[3] for i in xyz_data[2:atm_num+2]])]

# X and Y is the direct in the canves
if view_ang in ['+x','x']:
    print " |z\n+x -> y"
    X = np.array(xyz[1])
    Y = np.array(xyz[2])*-1
    Z = np.array(xyz[0])
elif view_ang in ['-x']:
    print " |z\n-x -> -y"
    X = np.array(xyz[1])*-1
    Y = np.array(xyz[2])*-1
    Z = np.array(xyz[0])*-1
elif view_ang in ['+y','y']:
    print " |z\n+y -> -x"
    X = np.array(xyz[0])*-1
    Y = np.array(xyz[2])*-1
    Z = np.array(xyz[1])
elif view_ang in ['-y']:
    print " |z\n-y -> x"
    X = np.array(xyz[0])
    Y = np.array(xyz[2])*-1
    Z = np.array(xyz[1])*-1
elif view_ang in ['+z','z']:
    print " |y\n+z -> x"
    X = np.array(xyz[0])
    Y = np.array(xyz[1])*-1
    Z = np.array(xyz[2])
elif view_ang in ['-z']:
    print " |y\n-z -> -x"
    X = np.array(xyz[0])*-1
    Y = np.array(xyz[1])*-1
    Z = np.array(xyz[2])*-1
else:
    print "Error: view angle would be in ±x, ±y or ±z"
    exit()

scale = max([(max(X) - min(X) + 2*max(radius_dic.values()))/(SIZE[0] - 2*MARGIN), 
             (max(Y) - min(Y) + 2*max(radius_dic.values()))/(SIZE[1] - 2*MARGIN)])

X = (X - min(X))/scale + MARGIN
X = X - (min(X)+max(X))/2 + SIZE[0]/2
Y = (Y - min(Y))/scale + MARGIN
Y = Y - (min(Y)+max(Y))/2 + SIZE[1]/2

# Init the canvas
canvas = Image.new("RGB", SIZE, "white") 
draw = ImageDraw.Draw(canvas) 

# draw bonds and atoms
data = np.array(zip(name,X,Y,Z))
data = data[np.lexsort(data.T)]
for i,j in combinations(data, 2):
    namei,xi,yi,zi = i
    xi = float(xi)
    yi = float(yi)
    zi = float(zi)
    namej,xj,yj,zj = j
    xj = float(xj)
    yj = float(yj)
    zj = float(zj)
    ri    = radius_dic[namei if namei in radius_dic.keys() else 'X']/scale
    rj    = radius_dic[namej if namej in radius_dic.keys() else 'X']/scale
    dist  = np.sqrt((xi-xj)**2 + (yi-yj)**2 + (zi-zj)**2)
    if dist < ri+rj:
        draw.line([(xi,yi),(xj,yj)], "black")
for n,x,y,z in data:
    x = float(x)
    y = float(y)
    r     = radius_dic[n if n in radius_dic.keys() else 'X']/scale
    color = color_dic [n if n in color_dic.keys()  else 'X']
    draw.ellipse((x-r, y-r, x+r, y+r), color, "black", width = 1)

# canvas.show() # for debuging
canvas.save(xyz_file.split('/')[-1].split('.')[0] + ".png") 

