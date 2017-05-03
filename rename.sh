#!/bin/bash

DIR="data/comments"

for file in $DIR/*.bz2
do
  bzip2 -d $file
  FILE=`echo "$file" | rev | cut -d'/' -f1 | rev | cut -d'.' -f1`
  if [[ $FILE == RC_20* ]]
  then
    NEWFILE=`echo "$FILE" | cut -d'_' -f2`
    mv $DIR/$FILE $DIR/$NEWFILE.txt
  fi
done
