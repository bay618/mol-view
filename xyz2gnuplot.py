#!/usr/bin/env python
#-*- coding: UTF-8 -*-

# For render the molecular structues from xyz-file to gnuplot script

import sys
import numpy as np
from itertools import combinations

# user defination for radius and color
radius_dic = {'H':0.5, 'X':0.9}   # in Ang
color_dic  = {'H' :[255,255,255], # white
              'Li':[  0,  0,255], # blue
              'C' :[ 63,191,191], # cyan
              'N' :[  0,  0,255], # blue
              'O' :[255,  0,  0], # red
              'F' :[  0,255,  0], # green
              'Na':[  0,  0,255], # blue,
              'S' :[255,255,  0], # yellow
              'Si':[255,255,  0], # yellow
              'Cl':[  0,255,  0], # green
              'K' :[  0,  0,255], # blue
              'Cs':[  0,  0,255], # blue
              'Al':[166,  0,166], # purple
              'Fe':[  0,  0,  0], # black
              'Cu':[255,127,  0], # orange
              'Au':[255,255,  0], # yellow
              'Pt':[ 76, 76, 76], # gray
              'X' :[ 76, 76, 76]} # gray

# parses the cmd options
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
    Y = np.array(xyz[2])
    Z = np.array(xyz[0])
elif view_ang in ['-x']:
    print " |z\n-x -> -y"
    X = np.array(xyz[1])*-1
    Y = np.array(xyz[2])
    Z = np.array(xyz[0])*-1
elif view_ang in ['+y','y']:
    print " |z\n+y -> -x"
    X = np.array(xyz[0])*-1
    Y = np.array(xyz[2])
    Z = np.array(xyz[1])
elif view_ang in ['-y']:
    print " |z\n-y -> x"
    X = np.array(xyz[0])
    Y = np.array(xyz[2])
    Z = np.array(xyz[1])*-1
elif view_ang in ['+z','z']:
    print " |y\n+z -> x"
    X = np.array(xyz[0])
    Y = np.array(xyz[1])
    Z = np.array(xyz[2])
elif view_ang in ['-z']:
    print " |y\n-z -> -x"
    X = np.array(xyz[0])*-1
    Y = np.array(xyz[1])
    Z = np.array(xyz[2])*-1
else:
    print "Error: view angle would be in ±x, ±y or ±z"
    exit()

SIZE = max([(max(X) - min(X) + 2*max(radius_dic.values())), 
            (max(Y) - min(Y) + 2*max(radius_dic.values()))])
x_max =(max(X)+min(X)+SIZE)/2
x_min =(max(X)+min(X)-SIZE)/2
y_max =(max(Y)+min(Y)+SIZE)/2
y_min =(max(Y)+min(Y)-SIZE)/2

# --- write the gnuplot script ---
f = open(xyz_file.split('/')[-1].split('.')[0] + '.gnuplot', 'w')
f.write("set term aqua size 300,300\n")
f.write("set style fill transparent solid 1.0 border -1\n")
f.write("set xrange [%.3f:%.3f]\n"%(x_min,x_max))
f.write("set yrange [%.3f:%.3f]\n"%(y_min,y_max))
f.write("unset key\n")
f.write("unset border\n")
f.write("unset xtics\n")
f.write("unset ytics\n")
f.write(r"rgb(r,g,b) = 65536 * int(r) + 256 * int(g) + int(b)"+"\n")
f.write(r"plot '-' using 1:2:3:(rgb($4,$5,$6)) with circles lc rgb var"+"\n")
f.write("    # X         Y      radiu   c_R c_G c_B      Z      name\n")
  
# draw atoms with circle
data = np.array(zip(name,X,Y,Z))
data = data[np.lexsort(data.T)]
for n,x,y,z in data:
    x = float(x)
    y = float(y)
    z = float(z)
    r     = radius_dic[n if n in radius_dic.keys() else 'X']
    color = color_dic [n if n in color_dic.keys()  else 'X']
    f.write("%10.3f%10.3f%8.2f  %4d%4d%4d%10.3f%6s\n"%(x,y,r,color[0],color[1],color[2],z,n))

f.write("END")
