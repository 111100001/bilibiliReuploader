#!/bin/bash

part="&p="

# Loop through each line in links.txt
for line in $(cat links.txt); do
  # Extract the bvid from the original URL (assuming it's a query parameter 'bvid=...')
  bvid=$(echo $line | sed -E 's/.*bvid=([^&]+).*/\1/')

  # Fetch the JSON from the URL and get the number of parts using jq
  num_pages=$(curl -s $line | jq '.data | length')

  # Loop through each part and append the part number to the URL
  for ((num = 1; num <= num_pages; num++)); do
    # Build the new URL in the desired format
    full_url="https://www.bilibili.com/video/$bvid?p=$num"

    # Append the full URL to all.txt
    echo "$full_url" >> all.txt
  done
done
