import re
import json
import os

# Path to the JSON file
json_file_path = "/home/ubuntu/bilibiliReuploader/my-tubeup-project/src/1_2_3_concatenated_1.mp4.info.json"

# Load the JSON file
# with open(json_file_path, 'r', encoding='utf-8') as f:
#     json_data = json.load(f)

# # Test the get_itemname function
# item_name = get_itemname(json_data)

# # Print the updated_data
# print(f"Generated item name: {item_name}")


def jsoner(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        original_data = json.load(f)
    display_id= ""
    title=""
    webpage_url=""
    extractor = original_data[0]['extractor']
    extractor_key = original_data[0]['extractor_key']
    upload_date = original_data[0]['upload_date']
    for video in original_data:
            #print(type(video))
        display_id += video['display_id'] + ' '
        title += video['title'] + ' '
        webpage_url += video['webpage_url'] + ' '
    
        
    print(f"Display ID: {display_id}")
    print(f"Title: {title}")
    print(f"Webpage URL: {webpage_url}")
    print(f"Extractor: {extractor}")
    print(f"Extractor Key: {extractor_key}")
    print(f"Upload Date: {upload_date}")

    new_data = {
        "extractor": extractor,
        "extractor_key": extractor_key,
        "upload_date": upload_date,
        "display_id": display_id.strip(),
        "title": title.strip(),
        "webpage_url": webpage_url.strip()
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
    

def concatenate_videos(video_dir, output_file="output.mp4"):
    concat_list_file = f"{video_dir}/concat_list.txt"
    files = os.listdir(video_dir)

    sorted_files = sorted(
    files,  
    #key=lambda x: int(re.search(r'_p(\d+)', x).group(1)) if re.search(r'_p(\d+)', x) else float('inf')
    key=lambda x: int(match.group(1)) if (match := re.search(r'_p(\d+)', x)) else float('inf')

)

    print(os.listdir(video_dir))
    with open(concat_list_file, 'w') as f:
        #used sorted() to make sure the videos are in order when written in the file
        for filename in sorted_files:

            if filename.endswith(".mp4"):
                if filename.count('_') <= 1: #if the upload fails and i run the script again, do not add the concatenated file in the text file
                    f.write(f"file '{filename}'\n")
                    print(f"file '{filename}'\n")
                    
                
    
    command = [  # noqa: F841
        "ffmpeg","-n",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_file,
        "-c", "copy",
        output_file, "-dry-run"
    ]
    #subprocess.run(command)

concatenate_videos("/home/ubuntu/bilibiliReuploader/my-tubeup-project/src/dd", "output.mp4")