#!/bin/bash

#remove carriage return and create new file with different name (name.txt+tmp)
for f in *
  do
    sed -e "s/[\r\n]//g" $f > $f+tmp
  done

#delete original file (*.txt)
rm *.txt

#change file type from .txt+tmp to .txt
ls | grep ".txt+tmp" | cut -d . -f 1 | while read line
do
  mv $line.txt+tmp $line.txt
done
