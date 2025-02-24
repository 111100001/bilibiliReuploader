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

def process_urls(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()  # Remove leading/trailing whitespace
            video_data = fetch_video_data(url)
            if video_data:
                # Extract video files and their durations from the JSON response
                video_files = []
                durations = []
                for video in video_data['data']:
                    video_files.append(video['part'])
                    durations.append(video['duration'])

                # Determine the most repeated duration
                most_common_duration = Counter(durations).most_common(1)[0][0]

                # Group files into streams
                streams = []
                current_stream = []
                current_duration = 0

                # Define the target duration and tolerance (e.g., ±10 seconds)
                target_duration = most_common_duration
                tolerance = 10  # ±10 seconds
                for i, file in enumerate(video_files):
                    file_path = file
                    duration_seconds = durations[i]
                    

                    current_stream.append(file_path)
                    current_duration = duration_seconds
                    
                        

                    # Check if the current duration is NOT approximately the target duration (± tolerance)
                    if (target_duration != current_duration ):
                        streams.append(current_stream)
                        current_stream = []
                        current_duration = 0

                # If there are remaining files in the current stream, add them
                if current_stream:
                    streams.append(current_stream)

                # Print the streams for verification
                print(streams + [' '] + [url])
                # for i, stream in enumerate(streams):
                #     print(f"Stream {i+1}:")
                #     for file in stream:
                #         print(f"  {file}  ")

# Example usage
process_urls('/home/ubuntu/links/links.txt')