"""Download and upload manager for video processing pipeline."""

import os
import time
from typing import List, Optional
import logging
from tubeup.TubeUp import TubeUp

logger = logging.getLogger("bilibiliReuploader.download_manager")


class DownloadManager:
    """Manages video downloads and uploads to Internet Archive."""
    
    def __init__(self, verbose: bool = True):
        self.tubeup = TubeUp(verbose=verbose)
    
    def download_videos(self, links: List[str], output_dir: str) -> Optional[set]:
        """
        Download videos using TubeUp.
        
        Args:
            links: List of video URLs to download
            output_dir: Directory to download videos to
            
        Returns:
            Set of downloaded video basenames, or None if failed
        """
        try:
            # Set the output directory
            self.tubeup.dir_path = output_dir
            
            logger.info(f"Starting download of {len(links)} videos to {output_dir}")
            
            # Download videos and get basenames
            downloaded_videos = self.tubeup.get_resource_basenames(
                links, 
                ignore_existing_item=True
            )
            
            logger.info(f"Successfully downloaded {len(downloaded_videos) if downloaded_videos else 0} videos")
            return downloaded_videos
            
        except Exception as e:
            logger.error(f"Failed to download videos: {e}")
            raise
    
    def upload_to_internet_archive(self, file_path: str) -> Optional[List[str]]:
        """
        Upload file to Internet Archive.
        
        Args:
            file_path: Path to file to upload
            
        Returns:
            List of uploaded filenames, or None if failed
        """
        try:
            logger.info(f"Starting upload to Internet Archive: {file_path}")
            
            uploaded_files = self.tubeup.upload_ia(file_path)
            
            if uploaded_files:
                logger.info(f"Successfully uploaded {len(uploaded_files)} files")
                logger.debug(f"Uploaded files: {uploaded_files}")
            else:
                logger.warning("Upload completed but no files were returned")
            
            return uploaded_files
            
        except Exception as e:
            logger.error(f"Failed to upload to Internet Archive: {e}")
            raise


class RetryManager:
    """Manages retry logic with exponential backoff."""
    
    def __init__(self, max_retries: int = 10, base_delay: int = 100):
        self.max_retries = max_retries
        self.base_delay = base_delay
    
    def execute_with_retry(self, func, *args, **kwargs):
        """
        Execute a function with retry logic.
        
        Args:
            func: Function to execute
            *args: Arguments to pass to function
            **kwargs: Keyword arguments to pass to function
            
        Returns:
            Function result
            
        Raises:
            Exception: If all retry attempts fail
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt == self.max_retries:
                    logger.error(f"All {self.max_retries + 1} attempts failed")
                    break
                
                delay = self.base_delay * (2 ** attempt)  # Exponential backoff
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
        
        # If we get here, all attempts failed
        raise last_exception