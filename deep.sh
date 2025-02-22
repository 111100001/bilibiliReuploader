#!/bin/bash

file="all.txt"  # Input file containing URLs
counter=0       # Counter for batch numbering

# Process the file in batches of 50 URLs
while IFS= read -r line1  && IFS= read -r line2  && IFS= read -r line3  && \
      IFS= read -r line4  && IFS= read -r line5  && IFS= read -r line6  && \
      IFS= read -r line7  && IFS= read -r line8  && IFS= read -r line9  && \
      IFS= read -r line10 && IFS= read -r line11 && IFS= read -r line12 && \
      IFS= read -r line13 && IFS= read -r line14 && IFS= read -r line15 && \
      IFS= read -r line16 && IFS= read -r line17 && IFS= read -r line18 && \
      IFS= read -r line19 && IFS= read -r line20 && IFS= read -r line21 && \
      IFS= read -r line22 && IFS= read -r line23 && IFS= read -r line24 && \
      IFS= read -r line25 && IFS= read -r line26 && IFS= read -r line27 && \
      IFS= read -r line28 && IFS= read -r line29 && IFS= read -r line30 && \
      IFS= read -r line31 && IFS= read -r line32 && IFS= read -r line33 && \
      IFS= read -r line34 && IFS= read -r line35 && IFS= read -r line36 && \
      IFS= read -r line37 && IFS= read -r line38 && IFS= read -r line39 && \
      IFS= read -r line40 && IFS= read -r line41 && IFS= read -r line42 && \
      IFS= read -r line43 && IFS= read -r line44 && IFS= read -r line45 && \
      IFS= read -r line46 && IFS= read -r line47 && IFS= read -r line48 && \
      IFS= read -r line49 && IFS= read -r line50; do

    ((counter++))  # Increment the batch counter

    dir="./dirs/$counter"
    mkdir -p "$dir"   # Ensure the directory exists
    cd "$dir" || exit  # Exit if `cd` fails

    # Create a script to process the current batch
    cat << EOF > "$counter.sh"
#!/bin/bash
tmux new-session -d -s $counter "yt-dlp -S +size,+br,+res,+fps \\
    $line1 $line2 $line3 $line4 $line5 $line6 $line7 $line8 $line9 $line10 \\
    $line11 $line12 $line13 $line14 $line15 $line16 $line17 $line18 $line19 $line20 \\
    $line21 $line22 $line23 $line24 $line25 $line26 $line27 $line28 $line29 $line30 \\
    $line31 $line32 $line33 $line34 $line35 $line36 $line37 $line38 $line39 $line40 \\
    $line41 $line42 $line43 $line44 $line45 $line46 $line47 $line48 $line49 $line50 \\
    && youtube-bulk-upload --yt_client_secrets_file /home/ubuntu/client_secret.json --noninteractive \\
    ;exec bash -i"
EOF

    chmod +x "$counter.sh"  # Make the script executable
    cd ../..  # Move back to the original directory

done < "$file"