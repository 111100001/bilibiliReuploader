#!/bin/bash

source ~/.bashrc
echo "Sourced ~/.bashrc" >> /tmp/bashrc_debug.log

TIME=86500
tet=5 
# Define timestamp file
TIMESTAMP_FILE="/tmp/last_run_time"

# Check if the file exists
if [ -f "$TIMESTAMP_FILE" ]; then
    last_run=$(cat "$TIMESTAMP_FILE")
    current_time=$(date +%s)
    
    # Calculate the time difference
    time_diff=$((current_time - last_run))
    
    # If less than 24 hours, wait until it's time
    if (( time_diff < $TIME )); then
        wait_time=$(($TIME - time_diff))
        echo "Waiting for $wait_time seconds until the next execution..."
        while (( wait_time > 0 )); do
            echo -ne "Time remaining: $wait_time seconds\r"
            sleep 1
            wait_time=$((wait_time - 1))
        done
        echo ""
    fi
fi

# Run your command here
echo "Running command..."

 /home/ubuntu/.local/bin/youtube-bulk-upload --yt_client_secrets_file /home/ubuntu/client_secret.json --noninteractive

# Update the timestamp
date +%s > "$TIMESTAMP_FILE"
