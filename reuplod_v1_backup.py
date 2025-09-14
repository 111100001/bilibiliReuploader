import os
import subprocess
import shutil
import re
from tubeup.TubeUp import TubeUp
import json
import time 


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
            match = re.search(r'https?://[^\s]+', line)
            if match:
                links.append(match.group())
    return links

# Step 2: Download videos using yt-dlp
tu = TubeUp(verbose=True)

def download_videos(links):

    set_of_downloaded_videos = tu.get_resource_basenames(links, ignore_existing_item=True)

   
    
        

# Step 3: Concatenate videos using ffmpeg
def concatenate_videos(video_dir, output_file="output.mp4"):
    concat_list_file = f"{video_dir}/concat_list.txt"
    files = os.listdir(video_dir)

    sorted_files = sorted(
    files,
    #key=lambda x: int(re.search(r'_p(\d+)', x).group(1)) if re.search(r'_p(\d+)', x) else float('inf')
    key=lambda x: int(match.group(1)) if (match := re.search(r'_p(\d+)', x)) else float('inf')
)

    with open(concat_list_file, 'w') as f:
        #used sorted() to make sure the videos are in order when written in the file
        for filename in sorted_files:
            if filename.endswith(".mp4"):
                if filename.count('_') <= 1: #if the upload fails and i run the script again, do not add the concatenated file in the text file
                    f.write(f"file '{filename}'\n")
                    
                
    
    command = [
        "ffmpeg","-stats", "-hide_banner", "-loglevel", "error", "-n",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_file,
        "-c", "copy",
        output_file
    ]
    subprocess.run(command)



# step 5: cleanup downloaded and concatenated files
def cleanup(video_dir):
    # Remove the directory and its contents
    if os.path.exists(video_dir):
        try:
            shutil.rmtree(video_dir)
            print(f"Deleted directory: {video_dir}")
        except Exception as e:
            print(f"Error deleting directory {video_dir}: {e}")
    else:
        print(f"Directory {video_dir} does not exist.")

        
# Function to sort filenames numerically
def sort_files_numerically(files):
    # Extract numbers from filenames and sort based on them
    def extract_number(filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else -1
    
    return sorted(files, key=extract_number)


def extract_and_join_part_numbers(file_path):
    part_numbers = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.search(r'\b\d+\b', line)
            if match:
                part_numbers.append(match.group())
    return ''.join(part_numbers)


def merge_json_files(input_dir, output_file):
    if os.path.exists(output_file):
        os.remove(output_file)  # Remove existing file if it exists
        print('merged json exists already, deleting it and creating a new one')
    merged_data = []

    # Iterate through all files in the input directory
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith(".json"):  # Process only JSON files
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)  # Load JSON data
                    merged_data.append(data)  # Append to the merged list
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in file {filename}: {e}")

    # Write the merged data to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=4, ensure_ascii=False)

    print(f"Merged JSON saved to {output_file}")

def strip_and_join_last_parts(urls):
    last_parts = [url.split('=')[-1] for url in urls if '=' in url]
    return '_'.join(last_parts).replace("\n","")

def jsoner(json_file):
    if not os.path.exists(json_file):
        print(f"File {json_file} does not exist.")
        return
    with open(json_file, 'r', encoding='utf-8') as f:
        original_data = json.load(f)
    
    if not isinstance(original_data, list):
        print('Concatenated JSON exists already, not merging')
        return
    
    display_id= ""
    title=""
    webpage_url=""
    extractor = original_data[0]['extractor']
    extractor_key = original_data[0]['extractor_key']
    upload_date = original_data[0]['upload_date']
    display_ids = []
    for video in original_data:
            #print(type(video))
        #display_id += video['display_id'] + ' '
        display_ids.append(video['display_id'])
        title += video['title'] + ' '
        webpage_url += video['webpage_url'] + ' '
    display_id_nums = [int(part.split('_p')[1]) for part in display_ids] # gets the numebrs after _p in identifiers
    display_id = display_ids[0] + '-' + str(max(display_id_nums))
    
    

    new_data = {
        "extractor": extractor,
        "extractor_key": extractor_key,
        "upload_date": upload_date,
        "display_id": display_id.strip(),
        "title": title.strip(),
        "webpage_url": webpage_url.strip(),
        "channel_url": "supertfLostMedia"
    }
    
    # Merge the new keys with the original originial_data
    if isinstance(original_data, list):
        # If the original original_data is a list, wrap it in a dictionary
        original_data = {"original_data": original_data}
    updated_data = {**new_data, **original_data}

    # Write the updated originial_data back to the original file
    with open(json_file, 'w', encoding='utf-8') as output_file:
        json.dump(updated_data, output_file, ensure_ascii=False, indent=4)
    
    print(f"Updated originial_data has been written to {json_file}")



def main():
    # Directory containing text files with video links
    directory = "/home/ubuntu/bilibiliReuploader/streams/failed"
    
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
            retry_delay = 100  # Delay in seconds between retries

            while True:  # Infinite retry loop
                try:
                    print(f"Processing file: {filename}")
                    
                    # Step 1: Extract video links
                    print("Extracting video links...")
                    video_links = extract_links(file_path)
                    print(f"Extracted {len(video_links)} video links.")
                    
                    # Step 2: Download videos
                    print("Downloading videos...")
                    video_dir = f"videos/videos_{filename[:-4]}"  # exclude last 4 chars
                    tu.dir_path = video_dir
                    download_videos(video_links)
                    print("Download complete.")
                    
                    # Step 3: Concatenate videos
                    print("Concatenating videos...")
                    output_file = f"{strip_and_join_last_parts(video_links)}_concatenated_{filename[:-4]}.mp4"  # Unique output file for each file
                    concatenate_videos(f"{video_dir}/downloads", f"{video_dir}/downloads/{output_file}")
                    print("Concatenation complete.")
                    
                    # Step 4: Merge JSON files and upload
                    input_directory = f"/home/ubuntu/bilibiliReuploader/{video_dir}/downloads"  # Directory containing JSON files
                    output_json_file = f"/home/ubuntu/bilibiliReuploader/{video_dir}/downloads/{output_file}.info.json"  # Output file path

                    merge_json_files(input_directory, output_json_file)
                    jsoner(output_json_file)
                    print("Uploading to Internet Archive...")
                    uploaded_file_names = tu.upload_ia(f"/home/ubuntu/bilibiliReuploader/{video_dir}/downloads/{output_file}")
                    print("Upload complete.")

                    # # Step 5: Cleanup
                    # if uploaded_file_names:
                    #     print("Cleaning up files...")
                    #     cleanup(video_dir)[]
                    #     print("Cleanup complete.")
                    
                    print(f"Finished processing file: {filename}\n")
                    
                    # Save the last processed file
                    save_last_processed(filename)

                    # Break out of the retry loop if successful
                    break

                except Exception as e:
                    print(f"Error processing file {filename}: {e}")
                    print(f"Retrying file {filename} after {retry_delay} seconds...")
                    time.sleep(retry_delay)  # Wait before retrying

if __name__ == "__main__":
    main()