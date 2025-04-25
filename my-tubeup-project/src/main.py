
import os
import subprocess
from tubeup.TubeUp import TubeUp
import yt_dlp
import json

def main():
    urls = 'https://www.bilibili.com/video/BV1dM4y1w7Vc'
        # Add more URLs as needed
    

    
    # ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(urls, download=False)

        # ℹ️ ydl.sanitize_info makes the info json-serializable
        #print(json.dumps(ydl.sanitize_info(info)))


    # Initialize the TubeUp instance
    tubeup = TubeUp(verbose=True, dir_path='.')

    # Example URLs to download and upload
    

    # Download and upload videos to archive.org
    #tubeup.get_resource_basenames(urls)
    #tubeup.upload_ia(urls)
    def concatenate_videos(video_dir = "/home/ubuntu/bilibiliReuploader/downloads", output_file="testing.mp4"):
        concat_list_file = "list.txt"
        listee= []
        with open(concat_list_file, 'w') as f:
            #used sorted() to make sure the videos are in order when written in the file
            for filename in sorted(os.listdir(video_dir)):
                if filename.endswith(".mp4"):
                    listee.append(filename)
                    f.write(f"file '{os.path.join(video_dir, filename)}'\n")
            print(listee)
        
        command = [
            "ffmpeg","-n",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_list_file,
            "-c", "copy",
            output_file
        ]
        subprocess.run(command)
    #concatenate_videos()

       

if __name__ == '__main__':
    main()