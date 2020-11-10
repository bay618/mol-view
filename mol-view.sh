#!/bin/bash

if [ $# -eq 1 ]; then
  view_ang='+z'
  filename=$1
  basename=`basename $filename`
elif [ $# -eq 2 ]; then
  view_ang=$1
  filename=$2
  basename=`basename $filename`
else
  echo "Usage: `basename $0` <±x/y/z> XYZ/POSCAR-file"
  exit
fi

if [ .${filename##*.} == .xyz ]; then
  xyz2png.py       $view_ang $filename
  viewer-cli.py    ${filename%.xyz}.png
  rm               ${filename%.xyz}.png
elif [ `basename $filename` == POSCAR -o `basename $filename` == CONTCAR ]; then
  poscar2xyz.py    $filename
  xyz2png.py       $view_ang POSCAR.xyz
  viewer-cli.py    POSCAR.png
  rm               POSCAR.xyz POSCAR.png
else
  echo "Usage: `basename $0` XYZ/POSCAR-file"
fi

