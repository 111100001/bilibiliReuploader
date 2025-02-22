#!/bin/bash

file="all.txt"
counter=0
scripts=()  # Array to store script paths

while true; do
    # Read 50 links into an array
    links=()
    for ((i=0; i<50; i++)); do
        if ! IFS= read -r line || [[ -z "$line" ]]; then
            break  # Stop if there are no more lines
        fi
        links+=("$line")
    done

    # Exit loop if no links were read
    if [[ ${#links[@]} -eq 0 ]]; then
        break
    fi

    ((counter++))  # Increment batch counter

    dir="./dirs/$counter"
    mkdir -p "$dir"  # Ensure the directory exists

    script_path="$dir/$counter.sh"
    scripts+=("$script_path")  # Store script path in array

    # Generate tmux script with each video being processed individually
    cat << EOF > "$script_path"
tmux new-session -d -s $counter ' \
for link in ${links[*]}; do \
    # Skip empty lines
    if [[ -z "\$link" ]]; then
        echo "Skipping empty link"
        continue
    fi

    # Download the video
    yt-dlp -S +size,+br,+res,+fps "\$link" && \

    # Find the latest video file (supports multiple formats)
    video_file=\$(ls -t *.{mp4,mkv,webm} 2>/dev/null | head -n 1) && \

    # Ensure a valid video file exists before uploading
    if [[ -f \"\$video_file\" ]]; then \
        youtube-bulk-upload --yt_client_secrets_file /home/ubuntu/client_secret.json --noninteractive \"\$video_file\" && \

        # Remove successfully uploaded video and URL from all.txt
        if [ \$? -eq 0 ]; then \
            sed -i \"/\$link/d\" $file && \
            rm -f \"\$video_file\"; \
        fi; \
    else \
        echo \"No video file found for \$link\"; \
    fi; \
done; exec bash -i'
EOF

    chmod +x "$script_path"  # Make the script executable
done < "$file"


