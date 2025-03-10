
import os
from tubeup.TubeUp import TubeUp

def main():
    # Initialize the TubeUp instance
    tubeup = TubeUp(verbose=True, dir_path='~/.tubeup')
    tubeup.dir_path='~/tessst'

    # Example URLs to download and upload
    urls = [
        'https://www.youtube.com/watch?v=TSOg8tNFlqo',
        # Add more URLs as needed
    ]

    # Download and upload videos to archive.org
    tubeup.get_resource_basenames(urls)
       

if __name__ == '__main__':
    main()