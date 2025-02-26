import os
import requests
from collections import Counter

def fetch_video_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from URL: {e}")
        return None
    except ValueError as e:
        print(f"Error decoding JSON: {e}")
        return None

def process_urls(item_name):
    with open(item_name, 'r') as item_name:
        for line in item_name:
            url = line.strip()  # Remove leading/trailing whitespace
            url_json_response = fetch_video_data(url)
            if url_json_response:
                # Extract video files and their durations from the JSON response
                anthology_item_names_list = []
                durations = []
                part_number= []
                for anthology_item in url_json_response['data']:
                    anthology_item_names_list.append(anthology_item['part'])
                    durations.append(anthology_item['duration'])
                    part_number.append(anthology_item['page'])

                # Determine the most repeated duration
                most_common_duration = Counter(durations).most_common(1)[0][0]

                # Group files into streams
                anthology_items_segmented_by_stream_day = []
                single_stream_segments_list = []
                current_duration = 0

                # Define the target duration and tolerance (e.g., ±10 seconds)
                target_duration = most_common_duration
                tolerance = 10  # ±10 seconds
                for index, item_name in enumerate(anthology_item_names_list):
                    duration_seconds = durations[index]
                    

                    single_stream_segments_list.append(item_name)
                    current_duration = duration_seconds
                    
                        

                    # Check if the current duration is NOT approximately the target duration (± tolerance)
                    if (target_duration != current_duration ):
                        anthology_items_segmented_by_stream_day.append(single_stream_segments_list)
                        single_stream_segments_list = []
                        current_duration = 0

                # If there are remaining files in the current stream, add them
                if single_stream_segments_list:
                    anthology_items_segmented_by_stream_day.append(single_stream_segments_list)

                # Print the streams for verification
                # print(anthology_items_segmented_by_stream_day + [' '] + [url])
                p_counter = 1
                with open('./grouped.txt', 'a') as f:
                    for i, stream in enumerate(anthology_items_segmented_by_stream_day):
                        f.write(f"Stream {i+1}:\n")
                        
                        for j, file in enumerate(stream):
                            # print(f"  {file} https://www.bilibili.com/video/{url[url.find('B'):].strip() if '=' in url else url.strip()}?p={ part_number[i] } ")
                            
                                f.write(f"  {file} https://www.bilibili.com/video/{url[url.find('B'):].strip() if '=' in url else url.strip()}?p={p_counter } \n")
                                p_counter += 1

                        
                        

# Example usage
process_urls('/home/ubuntu/links/links.txt')