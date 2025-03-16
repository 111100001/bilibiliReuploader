
import os
from tubeup.TubeUp import TubeUp

def main():
    # Initialize the TubeUp instance
    tubeup = TubeUp(verbose=True, dir_path='.')

    # Example URLs to download and upload
    urls = [
        'https://www.bilibili.com/video/BV15S4y1d77W?p=1',
        # Add more URLs as needed
    ]

    # Download and upload videos to archive.org
    tubeup.get_resource_basenames(urls)
    
    #tubeup.upload_ia(urls)
    
       

if __name__ == '__main__':
    main()