"""File operations and processing utilities."""

import os
import re
from typing import List, Optional
import logging

logger = logging.getLogger("bilibiliReuploader.file_processor")


class FileProcessor:
    """Handles file operations and link extraction."""
    
    def __init__(self, last_processed_file: str):
        self.last_processed_file = last_processed_file
    
    def read_last_processed(self) -> Optional[str]:
        """Read the last processed file name."""
        if os.path.exists(self.last_processed_file):
            try:
                with open(self.last_processed_file, 'r') as file:
                    return file.read().strip()
            except IOError as e:
                logger.error(f"Failed to read last processed file: {e}")
        return None
    
    def save_last_processed(self, filename: str) -> None:
        """Save the last processed file name."""
        try:
            with open(self.last_processed_file, 'w') as file:
                file.write(filename)
            logger.info(f"Saved last processed file: {filename}")
        except IOError as e:
            logger.error(f"Failed to save last processed file: {e}")
    
    def extract_links(self, file_path: str) -> List[str]:
        """
        Extract video links from a text file.
        
        Args:
            file_path: Path to the text file containing links
            
        Returns:
            List of extracted URLs
        """
        links = []
        try:
            with open(file_path, 'r') as file:
                for line_num, line in enumerate(file, 1):
                    match = re.search(r'https?://[^\s]+', line)
                    if match:
                        links.append(match.group())
                    elif line.strip():  # Non-empty line without URL
                        logger.warning(f"No URL found in line {line_num} of {file_path}")
            
            logger.info(f"Extracted {len(links)} links from {file_path}")
            return links
            
        except IOError as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            raise
    
    @staticmethod
    def sort_files_numerically(files: List[str]) -> List[str]:
        """
        Sort filenames numerically based on numbers found in the filename.
        
        Args:
            files: List of filenames to sort
            
        Returns:
            Sorted list of filenames
        """
        def extract_number(filename: str) -> int:
            match = re.search(r'\d+', filename)
            return int(match.group()) if match else -1
        
        return sorted(files, key=extract_number)
    
    @staticmethod
    def get_text_files(directory: str) -> List[str]:
        """
        Get all .txt files from a directory.
        
        Args:
            directory: Directory path to search
            
        Returns:
            List of .txt filenames
        """
        try:
            files = [f for f in os.listdir(directory) if f.endswith(".txt")]
            return FileProcessor.sort_files_numerically(files)
        except OSError as e:
            logger.error(f"Failed to list files in directory {directory}: {e}")
            raise