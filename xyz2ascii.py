#!/usr/bin/env python
#-*- coding: UTF-8 -*-

# For render the molecular structues from xyz-file to image

import sys
import time
import numpy as np

# user defination
SIZE   = (30, 20) # size of the canvas (w,h)
MARGIN =  1

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

# X and Y is the direct in the canvas
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

scale = max([(max(X) - min(X))/(SIZE[0] - 2*MARGIN), 
             (max(Y) - min(Y))/(SIZE[1] - 2*MARGIN)])

X = (X - min(X))/scale + MARGIN
X = X - (min(X)+max(X))/2 + SIZE[0]/2
Y = (Y - min(Y))/scale + MARGIN
Y = Y - (min(Y)+max(Y))/2 + SIZE[1]/2

# Init the canvas
canvas = [ [u"\u001b[48;5;15;38;5;15m  \u001b[0m"]*SIZE[0] for i in range(SIZE[1])]

# draw each atoms
data = np.array(zip(name,X,Y,Z), dtype='|S32')
data = data[np.lexsort(data.T)]
for n,x,y,z in data:
    z = int((max(Z)-float(z))/(max(Z)-min(Z))*20+232) if max(Z)-min(Z) > 0.1 else 232
    canvas[int(float(y))][int(float(x))] = u"\u001b[48;5;15;38;5;%dm%-2s\u001b[0m"%(z,n)

# print the canvas
for line in [''.join(s) for s in canvas]:
    print line


### a patch for trajories ####################################
numframes = len(xyz_data)/(atm_num+2)

for framei in range(1, numframes):
    xyz  = [map(float, [i[0:-1].split()[1] for i in xyz_data[2+(atm_num+2)*framei:(atm_num+2)*(framei+1)]]),
            map(float, [i[0:-1].split()[2] for i in xyz_data[2+(atm_num+2)*framei:(atm_num+2)*(framei+1)]]),
            map(float, [i[0:-1].split()[3] for i in xyz_data[2+(atm_num+2)*framei:(atm_num+2)*(framei+1)]])]

    # X and Y is the direct in the canvas
    if view_ang in ['+x','x']:
        X = np.array(xyz[1])
        Y = np.array(xyz[2])*-1
        Z = np.array(xyz[0])
    elif view_ang in ['-x']:
        X = np.array(xyz[1])*-1
        Y = np.array(xyz[2])*-1
        Z = np.array(xyz[0])*-1
    elif view_ang in ['+y','y']:
        X = np.array(xyz[0])*-1
        Y = np.array(xyz[2])*-1
        Z = np.array(xyz[1])
    elif view_ang in ['-y']:
        X = np.array(xyz[0])
        Y = np.array(xyz[2])*-1
        Z = np.array(xyz[1])*-1
    elif view_ang in ['+z','z']:
        X = np.array(xyz[0])
        Y = np.array(xyz[1])*-1
        Z = np.array(xyz[2])
    elif view_ang in ['-z']:
        X = np.array(xyz[0])*-1
        Y = np.array(xyz[1])*-1
        Z = np.array(xyz[2])*-1
    
    X = (X - min(X))/scale + MARGIN
    X = X - (min(X)+max(X))/2 + SIZE[0]/2
    Y = (Y - min(Y))/scale + MARGIN
    Y = Y - (min(Y)+max(Y))/2 + SIZE[1]/2

    # Init the canvas
    canvas = [ [u"\u001b[48;5;15;38;5;15m  \u001b[0m"]*SIZE[0] for i in range(SIZE[1])]

    # draw each atoms
    data = np.array(zip(name,X,Y,Z), dtype='|S32')
    data = data[np.lexsort(data.T)]
    for n,x,y,z in data:
        if 0<=int(float(x))<SIZE[0] and 0<=int(float(y))<SIZE[1]:
            z = int((max(Z)-float(z))/(max(Z)-min(Z))*20+232) if max(Z)-min(Z) > 0.1 else 232
            canvas[int(float(y))][int(float(x))] = u"\u001b[48;5;15;38;5;%dm%-2s\u001b[0m"%(z,n)
    
    # print the canvas 
    print u"\u001b[%dA\u001b[%dC [frame %d/%d]"%(SIZE[1]+1,2*SIZE[0]-20,framei+1,numframes)
    for line in [''.join(s) for s in canvas]:
        print line
    if numframes < 500:
        time.sleep(5./numframes)
