#!/bin/bash

line='https://www.bilibili.com/video/BV1554y1b76i?p=1'
id="$(echo "$line" | sed -E 's|.*/video/([^/?]+).*|\1|')"
#for line in $(cat all.txt)
#do
  if [ -d $id ]; then
    :
  else 
    mkdir "$id"
  fi 

  cd "$id"
   
  tmux new-session  -s "$id" "yt-dlp -s "$line"" 
  cd ..  
#done
