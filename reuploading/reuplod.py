import os
import subprocess
from internetarchive import upload
import shutil
import re

LAST_PROCESSED_FILE = "last_processed.txt"

# Function to read the last processed file
def read_last_processed():
    if os.path.exists(LAST_PROCESSED_FILE):
        with open(LAST_PROCESSED_FILE, 'r') as file:
            return file.read().strip()
    return None

# Function to save the last processed file
def save_last_processed(filename):
    with open(LAST_PROCESSED_FILE, 'w') as file:
        file.write(filename)

# Step 1: Extract video links from a single text file
def extract_links(file_path):
    links = []
    with open(file_path, 'r') as file:
        for line in file:
            if "bilibili.com" in line:
                # Remove any leading numbers or spaces
                cleaned_line = line.lstrip("0123456789. ")
                links.append(cleaned_line.strip())
    return links

# Step 2: Download videos using yt-dlp
def download_videos(links, output_dir="videos"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for link in links:
        command = [
            "yt-dlp",
            "-o", f"{output_dir}/%(title)s.%(ext)s",
            link,
            "--download-archive", "archive.log",
            "-S", "+size,+br,+res,+fps"
        ]
        subprocess.run(command)
        

# Step 3: Concatenate videos using ffmpeg
def concatenate_videos(video_dir, output_file="output.mp4"):
    concat_list_file = "concat_list.txt"
    print(os.listdir(video_dir))
    with open(concat_list_file, 'w') as f:
        #used sorted() to make sure the videos are in order when written in the file
        for filename in sorted(os.listdir(video_dir)):
            if filename.endswith(".mp4"):
                f.write(f"file '{os.path.join(video_dir, filename)}'\n")
    
    command = [
        "ffmpeg","-n",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_file,
        "-c", "copy",
        output_file
    ]
    subprocess.run(command)

# Step 4: Upload to Internet Archive
def upload_to_archive(file_path, title, description, collection="opensource"):
    item = upload(f"{title}", files=[file_path], metadata={
        "title": title,
        "description": description,
        "collection": collection,
        "mediatype": "movies",
    }, retries=9001,
                    request_kwargs=dict(timeout=(9001, 9001)), verbose=True)
    return item

# Step 5: Cleanup downloaded and concatenated files
def cleanup(video_dir, concat_list_file, output_file):
    # Delete the downloaded videos directory
    if os.path.exists(video_dir):
        try:
            shutil.rmtree(video_dir)
            print(f"Deleted directory: {video_dir}")
        except Exception as e:
            print(f"Error deleting directory {video_dir}: {e}")
    else:
        print(f"Directory {video_dir} does not exist.")
    
    # Delete the concatenation list file
    if os.path.exists(concat_list_file):
        try:
            os.remove(concat_list_file)
            print(f"Deleted file: {concat_list_file}")
        except Exception as e:
            print(f"Error deleting file {concat_list_file}: {e}")
    else:
        print(f"File {concat_list_file} does not exist.")
    
    # Delete the concatenated video file
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
            print(f"Deleted file: {output_file}")
        except Exception as e:
            print(f"Error deleting file {output_file}: {e}")
    else:
        print(f"File {output_file} does not exist.")
        
# Function to sort filenames numerically
def sort_files_numerically(files):
    # Extract numbers from filenames and sort based on them
    def extract_number(filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else -1
    
    return sorted(files, key=extract_number)

import re

def extract_and_join_identifiers(file_path):
    identifiers = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'\b\d+\b', line)
            if match:
                identifiers.append(match.group())
    return ''.join(identifiers)

# Main function to process each file one at a time
def main():
    # Directory containing text files with video links
    directory = "/home/ubuntu/links/streams"
    
    # Get list of files and sort them numerically
    files = [f for f in os.listdir(directory) if f.endswith(".txt")]
    sorted_files = sort_files_numerically(files)
    
    # Read the last processed file
    last_processed = read_last_processed()
    start_index = 0
    if last_processed:
        try:
            start_index = sorted_files.index(last_processed) + 1
        except ValueError:
            pass
    
    # Process each file in the directory starting from the last processed file
    for filename in sorted_files[start_index:]:
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            print(f"Processing file: {filename}")
            
            # Step 1: Extract video links
            print("Extracting video links...")
            video_links = extract_links(file_path)
            print(f"Extracted {len(video_links)} video links.")
            
            # Step 2: Download videos
            print("Downloading videos...")
            video_dir = f"videos_{filename[:-4]}"  # Unique folder for each file
            download_videos(video_links, video_dir)
            print("Download complete.")
            
            # Step 3: Concatenate videos
            print("Concatenating videos...")
            output_file = f"output_{filename[:-4]}.mp4"  # Unique output file for each file
            concat_list_file = f"concat_list_{filename[:-4]}.txt"  # Unique concat list for each file
            concatenate_videos(video_dir, output_file)
            print("Concatenation complete.")
            
            # Step 4: Upload to Internet Archive
            print("Uploading to Internet Archive...")
            identifier = extract_and_join_identifiers(file_path)
            title = f"{identifier}-{filename[:-4]}-BiliBili"
            description = f"A collection of videos downloaded from Bilibili and concatenated into a single file from {filename}."
            upload_to_archive(output_file, title, description)
            print("Upload complete.")
            
            # Step 5: Cleanup
            print("Cleaning up files...")
            cleanup(video_dir, concat_list_file, output_file)
            print("Cleanup complete.")
            
            print(f"Finished processing file: {filename}\n")
            
            # Save the last processed file
            save_last_processed(filename)

if __name__ == "__main__":
    main()