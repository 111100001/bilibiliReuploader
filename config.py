"""Configuration management for bilibiliReuploader."""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class Config:
    """Application configuration."""
    
    # Directories
    streams_directory: str = "/home/ubuntu/bilibiliReuploader/streams/failed"
    videos_directory: str = "videos"
    
    # File names
    last_processed_file: str = "last_processed.txt"
    
    # Retry settings
    retry_delay: int = 100  # seconds
    max_retries: int = 10
    
    # Video processing
    ffmpeg_loglevel: str = "error"
    concatenated_suffix: str = "_concatenated"
    
    # Internet Archive
    ia_collection: str = "supertfLostMedia"
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Create configuration from environment variables."""
        return cls(
            streams_directory=os.getenv('STREAMS_DIR', cls.streams_directory),
            videos_directory=os.getenv('VIDEOS_DIR', cls.videos_directory),
            last_processed_file=os.getenv('LAST_PROCESSED_FILE', cls.last_processed_file),
            retry_delay=int(os.getenv('RETRY_DELAY', str(cls.retry_delay))),
            max_retries=int(os.getenv('MAX_RETRIES', str(cls.max_retries))),
            ffmpeg_loglevel=os.getenv('FFMPEG_LOGLEVEL', cls.ffmpeg_loglevel),
            ia_collection=os.getenv('IA_COLLECTION', cls.ia_collection),
        )