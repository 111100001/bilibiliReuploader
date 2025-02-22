import os
import subprocess
from datetime import timedelta

# Directory containing the video files
video_dir = "/home/ubuntu/links/dirs/7"

# Get list of video files sorted by name
video_files = sorted([f for f in os.listdir(video_dir) if f.endswith(".mp4")])

# Function to get duration of a video file using ffmpeg
def get_duration(file_path):
    result = subprocess.run(
        ["ffmpeg", "-i", file_path],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    duration_line = [line for line in result.stderr.decode().split("\n") if "Duration" in line][0]
    duration_str = duration_line.split(",")[0].split(" ")[-1]
    return duration_str

# Function to convert duration string (HH:MM:SS.ss) to seconds
def duration_to_seconds(duration_str):
    hours, minutes, seconds = duration_str.split(":")
    seconds = float(seconds)
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds)

# Group files into streams
streams = []
current_stream = []

# Define the target duration (2 hours in seconds) and tolerance (e.g., ±10 seconds)
target_duration = 7200  # 2 hours in seconds
tolerance = 10  # ±10 seconds

for file in video_files:
    file_path = os.path.join(video_dir, file)
    duration_str = get_duration(file_path)
    duration_seconds = duration_to_seconds(duration_str)
    
    current_stream.append(file_path)
    
    # Check if the duration is NOT approximately 2 hours (± tolerance)
    if not (target_duration - tolerance <= duration_seconds <= target_duration + tolerance):
        streams.append(current_stream)
        current_stream = []

# If there are remaining files in the current stream, add them
if current_stream:
    streams.append(current_stream)

# Write the grouped files into text files
for i, stream in enumerate(streams):
    with open(f"stream_{i+1}_files.txt", "w") as f:
        for file in stream:
            f.write(f"file '{file}'\n")
    print(f"Created stream_{i+1}_files.txt with {len(stream)} files.")

# Print the streams for verification
for i, stream in enumerate(streams):
    print(f"Stream {i+1}:")
    for file in stream:
        print(f"  {file}")
