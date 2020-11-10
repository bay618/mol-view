#!/usr/bin/env python
import sys
import numpy as np

if len(sys.argv) == 1:
    poscar_file = open("POSCAR", "r").readlines()
elif len(sys.argv) == 2:
    poscar_file = open(sys.argv[1], "r").readlines()
else:
    print "Usage: %s POSCAR_file" % sys.argv[0]
    exit()

lattice_1 = np.array(map(float, poscar_file[2].split()))
lattice_2 = np.array(map(float, poscar_file[3].split()))
lattice_3 = np.array(map(float, poscar_file[4].split()))
name_list = poscar_file[5].split()
n_list    = map(int, poscar_file[6].split())
s_flag    = 1 if poscar_file[7][0] in 'Ss' else 0
number    = sum(n_list) # total number of ions

NAME = []
for name_i,n_i in zip(name_list, n_list):
    NAME += [name_i] * n_i

X, Y, Z = [], [], []
for i in range(number):
    if poscar_file[7+s_flag][0] in 'Cc':
        X.append(float(poscar_file[8 + s_flag + i].split()[0]))
        Y.append(float(poscar_file[8 + s_flag + i].split()[1]))
        Z.append(float(poscar_file[8 + s_flag + i].split()[2]))
    elif poscar_file[7+s_flag][0] in 'Dd':
        d1 = float(poscar_file[8 + s_flag + i].split()[0])
        d2 = float(poscar_file[8 + s_flag + i].split()[1])
        d3 = float(poscar_file[8 + s_flag + i].split()[2])
        X.append(d1*lattice_1[0] + d2*lattice_2[0] + d3*lattice_3[0])
        Y.append(d1*lattice_1[1] + d2*lattice_2[1] + d3*lattice_3[1])
        Z.append(d1*lattice_1[2] + d2*lattice_2[2] + d3*lattice_3[2])

xyz_file = open(sys.argv[1] if len(sys.argv) == 2 else "POSCAR" + ".xyz", "w")
xyz_file.write("%d\n  by poscar2xyz.py\n"%(number))
for i in range(number):
    xyz_file.write("%s  %10.6f %10.6f %10.6f\n"%(NAME[i],X[i],Y[i],Z[i]))
xyz_file.close()

