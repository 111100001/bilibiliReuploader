#!/bin/bash

echo "type the link here"

read link
lastpart=$(basename "$link")
mkdir "$lastpart"
cd "$lastpart"
tmux new -s "$lastpart" -d
tmux send-keys -t "$lastpart" "yt-dlp  \"$link\"" C-m


