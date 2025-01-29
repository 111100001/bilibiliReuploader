#!/bin/bash

file="all.txt"
counter=0

while IFS= read -r line1 && IFS= read -r line2 && IFS= read -r line3 && \
IFS= read -r line4 && IFS= read -r line5 && IFS= read -r line6 && \
IFS= read -r line7 && IFS= read -r line8 && \
IFS= read -r line9 && IFS= read -r line10 && IFS= read -r line11; do
    ((counter++))
    
    dir="./dirs/$counter"
    mkdir -p "$dir"   # Ensure the directory exists
    cd "$dir" || exit  # Exit if `cd` fails

    cat << EOF > "$counter.sh"
#!/bin/bash
tmux new-session -d -s $counter "yt-dlp -S +size,+br,+res,+fps $line1 $line2 $line3 $line4 $line5 $line6 $line7 $line8 $line9 $line10 $line11 && \
youtube-bulk-upload --yt_client_secrets_file /home/ubuntu/client_secret.json --noninteractive && sudo rm -r *.mp4; exec bash -i"
EOF

    chmod +x "$counter.sh"  # Make the script executable
    cd ../..  # Move back to original directory
done < "$file"
