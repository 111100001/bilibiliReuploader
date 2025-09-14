"""Video processing utilities for concatenation and ffmpeg operations."""

import os
import subprocess
import re
import shutil
from typing import List
import logging

logger = logging.getLogger("bilibiliReuploader.video_processor")


class VideoProcessor:
    """Handles video concatenation and processing operations."""
    
    def __init__(self, ffmpeg_loglevel: str = "error"):
        self.ffmpeg_loglevel = ffmpeg_loglevel
    
    def concatenate_videos(self, video_dir: str, output_file: str) -> None:
        """
        Concatenate videos using ffmpeg.
        
        Args:
            video_dir: Directory containing video files
            output_file: Output file path for concatenated video
        """
        concat_list_file = os.path.join(video_dir, "concat_list.txt")
        
        try:
            files = os.listdir(video_dir)
            sorted_files = self._sort_video_files(files)
            
            # Create concat list file
            with open(concat_list_file, 'w') as f:
                for filename in sorted_files:
                    if filename.endswith(".mp4") and self._is_valid_video_file(filename):
                        f.write(f"file '{filename}'\n")
            
            # Run ffmpeg command
            command = [
                "ffmpeg", "-stats", "-hide_banner", 
                "-loglevel", self.ffmpeg_loglevel, "-n",
                "-f", "concat", "-safe", "0",
                "-i", concat_list_file,
                "-c", "copy", output_file
            ]
            
            logger.info(f"Starting video concatenation: {output_file}")
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Successfully concatenated videos to {output_file}")
            else:
                logger.error(f"FFmpeg failed with return code {result.returncode}")
                logger.error(f"Error output: {result.stderr}")
                raise subprocess.CalledProcessError(result.returncode, command)
                
        except Exception as e:
            logger.error(f"Failed to concatenate videos: {e}")
            raise
        finally:
            # Clean up concat list file
            if os.path.exists(concat_list_file):
                os.remove(concat_list_file)
    
    def _sort_video_files(self, files: List[str]) -> List[str]:
        """Sort video files by part number."""
        return sorted(
            files,
            key=lambda x: int(match.group(1)) if (match := re.search(r'_p(\d+)', x)) else float('inf')
        )
    
    def _is_valid_video_file(self, filename: str) -> bool:
        """
        Check if file is a valid video file for concatenation.
        
        Excludes already concatenated files based on underscore count.
        """
        return filename.count('_') <= 1
    
    def cleanup_directory(self, video_dir: str) -> None:
        """
        Remove video directory and its contents.
        
        Args:
            video_dir: Directory path to remove
        """
        if os.path.exists(video_dir):
            try:
                shutil.rmtree(video_dir)
                logger.info(f"Deleted directory: {video_dir}")
            except Exception as e:
                logger.error(f"Error deleting directory {video_dir}: {e}")
        else:
            logger.warning(f"Directory {video_dir} does not exist.")
    
    @staticmethod
    def generate_output_filename(video_links: List[str], base_filename: str, suffix: str = "_concatenated") -> str:
        """
        Generate output filename from video links and base filename.
        
        Args:
            video_links: List of video URLs
            base_filename: Base filename without extension
            suffix: Suffix to append
            
        Returns:
            Generated output filename
        """
        url_parts = VideoProcessor._extract_url_parts(video_links)
        return f"{url_parts}{suffix}_{base_filename}.mp4"
    
    @staticmethod
    def _extract_url_parts(urls: List[str]) -> str:
        """Extract and join the last parts of URLs after '=' character."""
        last_parts = [url.split('=')[-1] for url in urls if '=' in url]
        return '_'.join(last_parts).replace("\n", "")