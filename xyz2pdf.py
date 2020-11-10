#!/usr/bin/env python
#-*- coding: UTF-8 -*-

# For render the molecular structues from xyz-file to tex/tikz file

import os,sys
import numpy as np
from itertools import combinations

# user defination
radius_dic = {'H':0.5, 'X':0.8} # in Ang
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

max_XY = max([max(X)-min(X), max(Y)-min(Y)])

# Print into the tex/tikz file
basename = xyz_file[:-4].split('/')[-1]
tikz_f = open(basename+'.tex', 'w')
tikz_f.write("""\
\\documentclass{article}
\\usepackage{geometry}
\\geometry{paperwidth=%fcm, paperheight=%fcm,left=1.5cm,right=1.5cm,top=1.5cm,bottom=1.5cm}
\\pagestyle{empty}
 
\\usepackage{tikz}
\\begin{document}
  \\centering
  \\begin{tikzpicture}
"""%(1.2*max_XY,1.2*max_XY))

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
    ri    = radius_dic[namei if namei in radius_dic.keys() else 'X']
    rj    = radius_dic[namej if namej in radius_dic.keys() else 'X']
    dist  = np.sqrt((xi-xj)**2 + (yi-yj)**2 + (zi-zj)**2)
    if dist < (ri+rj):
        tikz_f.write("  \\draw[-, thick] (%8.3f,%8.3f) -- (%8.3f,%8.3f);\n"%(xi,yi,xj,yj))

for n,x,y,z in data:
    x = float(x)
    y = float(y)
    r     = radius_dic[n if n in radius_dic.keys() else 'X']
    color = color_dic [n if n in color_dic.keys()  else 'X']
    tikz_f.write("  \\draw[fill=%-6s, very thick] (%8.3f,%8.3f) circle (%.2f); %% %s \n"%(color,x,y,r,n))

tikz_f.write("""\
  \\end{tikzpicture}
\\end{document}
""")

tikz_f.close()

os.system("pdflatex %s.tex"%basename)
os.system("rm %s.log %s.aux"%(basename,basename))


