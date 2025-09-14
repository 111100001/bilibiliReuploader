"""Main application class for bilibiliReuploader."""

import os
from typing import List, Optional
import logging

from config import Config
from file_processor import FileProcessor
from video_processor import VideoProcessor
from json_processor import JsonProcessor
from download_manager import DownloadManager, RetryManager

logger = logging.getLogger("bilibiliReuploader.app")


class BilibiliReuploader:
    """Main application class for processing and re-uploading Bilibili videos."""
    
    def __init__(self, config: Config):
        self.config = config
        self.file_processor = FileProcessor(config.last_processed_file)
        self.video_processor = VideoProcessor(config.ffmpeg_loglevel)
        self.json_processor = JsonProcessor()
        self.download_manager = DownloadManager()
        self.retry_manager = RetryManager(config.max_retries, config.retry_delay)
    
    def run(self) -> None:
        """Run the main processing loop."""
        logger.info("Starting bilibiliReuploader")
        
        try:
            files = self._get_files_to_process()
            
            for filename in files:
                self._process_file_with_retry(filename)
                
        except Exception as e:
            logger.error(f"Application failed: {e}")
            raise
        
        logger.info("bilibiliReuploader completed successfully")
    
    def _get_files_to_process(self) -> List[str]:
        """Get list of files to process, starting from last processed file."""
        files = self.file_processor.get_text_files(self.config.streams_directory)
        
        # Find starting point based on last processed file
        last_processed = self.file_processor.read_last_processed()
        start_index = 0
        
        if last_processed:
            try:
                start_index = files.index(last_processed) + 1
                logger.info(f"Resuming from file index {start_index} after {last_processed}")
            except ValueError:
                logger.warning(f"Last processed file {last_processed} not found, starting from beginning")
        
        return files[start_index:]
    
    def _process_file_with_retry(self, filename: str) -> None:
        """Process a single file with retry logic."""
        logger.info(f"Processing file: {filename}")
        
        def process_func():
            return self._process_file(filename)
        
        try:
            self.retry_manager.execute_with_retry(process_func)
            self.file_processor.save_last_processed(filename)
            logger.info(f"Successfully completed processing: {filename}")
        except Exception as e:
            logger.error(f"Failed to process file {filename} after all retries: {e}")
            raise
    
    def _process_file(self, filename: str) -> None:
        """Process a single file through the complete pipeline."""
        file_path = os.path.join(self.config.streams_directory, filename)
        
        # Step 1: Extract video links
        video_links = self.file_processor.extract_links(file_path)
        if not video_links:
            logger.warning(f"No video links found in {filename}")
            return
        
        # Step 2: Set up directories
        base_name = filename[:-4]  # Remove .txt extension
        video_dir = os.path.join(self.config.videos_directory, f"videos_{base_name}")
        downloads_dir = os.path.join(video_dir, "downloads")
        
        try:
            # Step 3: Download videos
            self.download_manager.download_videos(video_links, video_dir)
            
            # Step 4: Generate output filename and concatenate
            output_filename = self.video_processor.generate_output_filename(
                video_links, base_name, self.config.concatenated_suffix
            )
            output_path = os.path.join(downloads_dir, output_filename)
            
            self.video_processor.concatenate_videos(downloads_dir, output_path)
            
            # Step 5: Process JSON metadata
            json_output_path = f"{output_path}.info.json"
            self.json_processor.merge_json_files(downloads_dir, json_output_path)
            self.json_processor.process_concatenated_metadata(
                json_output_path, self.config.ia_collection
            )
            
            # Step 6: Upload to Internet Archive
            uploaded_files = self.download_manager.upload_to_internet_archive(output_path)
            
            # Step 7: Cleanup (commented out in original, keeping same behavior)
            # if uploaded_files:
            #     self.video_processor.cleanup_directory(video_dir)
            
        except Exception as e:
            logger.error(f"Error in processing pipeline for {filename}: {e}")
            raise


class ApplicationFactory:
    """Factory class for creating application instances."""
    
    @staticmethod
    def create_from_config(config: Optional[Config] = None) -> BilibiliReuploader:
        """
        Create application instance from configuration.
        
        Args:
            config: Configuration instance, or None to load from environment
            
        Returns:
            Configured BilibiliReuploader instance
        """
        if config is None:
            config = Config.from_env()
        
        return BilibiliReuploader(config)