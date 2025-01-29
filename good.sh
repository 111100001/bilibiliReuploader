#!/bin/bash

file="all.txt"
counter=0
scripts=()  # Array to store script paths

while true; do
    # Read 50 lines into an array
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

    # Generate tmux script with all 50 links
    cat << EOF > "$script_path"
#!/bin/bash
tmux new-session -d -s $counter "yt-dlp -S +size,+br,+res,+fps ${links[*]} && \
youtube-bulk-upload --yt_client_secrets_file /home/ubuntu/client_secret.json --noninteractive && sudo rm -r *.mp4; exec bash -i"
EOF

    chmod +x "$script_path"  # Make the script executable
done < "$file"