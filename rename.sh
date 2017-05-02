#!/bin/bash

DIR="data/comments"

for file in $DIR/*.bz2
do
  FILE=`echo "$file" | rev | cut -d'/' -f1 | rev`
  if [[ $FILE == RC_20*.bz2 ]]
  then
    NEWFILE=`echo "$FILE" | cut -d'_' -f2 | cut -d'.' -f1`
    mv $DIR/$FILE $DIR/$NEWFILE.txt
  fi
done
