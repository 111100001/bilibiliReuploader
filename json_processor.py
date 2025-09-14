"""JSON metadata processing utilities."""

import os
import json
import re
from typing import List, Dict, Any
import logging

logger = logging.getLogger("bilibiliReuploader.json_processor")


class JsonProcessor:
    """Handles JSON metadata processing and merging operations."""
    
    def merge_json_files(self, input_dir: str, output_file: str) -> None:
        """
        Merge all JSON files in a directory into a single file.
        
        Args:
            input_dir: Directory containing JSON files
            output_file: Output file path for merged JSON
        """
        if os.path.exists(output_file):
            os.remove(output_file)
            logger.info('Existing merged JSON file deleted, creating new one')
        
        merged_data = []
        
        try:
            for filename in sorted(os.listdir(input_dir)):
                if filename.endswith(".json"):
                    file_path = os.path.join(input_dir, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            merged_data.append(data)
                    except json.JSONDecodeError as e:
                        logger.error(f"Error decoding JSON in file {filename}: {e}")
                    except IOError as e:
                        logger.error(f"Error reading file {filename}: {e}")
            
            # Write merged data
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(merged_data, f, indent=4, ensure_ascii=False)
            
            logger.info(f"Merged {len(merged_data)} JSON files into {output_file}")
            
        except Exception as e:
            logger.error(f"Failed to merge JSON files: {e}")
            raise
    
    def process_concatenated_metadata(self, json_file: str, collection: str = "supertfLostMedia") -> None:
        """
        Process and update JSON metadata for concatenated videos.
        
        Args:
            json_file: Path to JSON file to process
            collection: Internet Archive collection name
        """
        if not os.path.exists(json_file):
            logger.error(f"File {json_file} does not exist.")
            return
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                original_data = json.load(f)
            
            # Skip if already processed
            if not isinstance(original_data, list):
                logger.info('JSON metadata already processed, skipping')
                return
            
            # Extract metadata from video list
            metadata = self._extract_combined_metadata(original_data, collection)
            
            # Merge with original data
            updated_data = {**metadata, "original_data": original_data}
            
            # Write back to file
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, ensure_ascii=False, indent=4)
            
            logger.info(f"Updated metadata written to {json_file}")
            
        except Exception as e:
            logger.error(f"Failed to process JSON metadata: {e}")
            raise
    
    def _extract_combined_metadata(self, video_list: List[Dict[str, Any]], collection: str) -> Dict[str, Any]:
        """
        Extract and combine metadata from a list of video metadata objects.
        
        Args:
            video_list: List of video metadata dictionaries
            collection: Collection name for channel_url
            
        Returns:
            Combined metadata dictionary
        """
        if not video_list:
            raise ValueError("Empty video list provided")
        
        first_video = video_list[0]
        
        # Combine titles and URLs
        combined_title = ' '.join(video['title'] for video in video_list).strip()
        combined_webpage_url = ' '.join(video['webpage_url'] for video in video_list).strip()
        
        # Extract display IDs and generate combined display ID
        display_ids = [video['display_id'] for video in video_list]
        combined_display_id = self._generate_combined_display_id(display_ids)
        
        return {
            "extractor": first_video['extractor'],
            "extractor_key": first_video['extractor_key'],
            "upload_date": first_video['upload_date'],
            "display_id": combined_display_id,
            "title": combined_title,
            "webpage_url": combined_webpage_url,
            "channel_url": collection
        }
    
    def _generate_combined_display_id(self, display_ids: List[str]) -> str:
        """
        Generate a combined display ID from a list of display IDs.
        
        Args:
            display_ids: List of video display IDs
            
        Returns:
            Combined display ID in format "first_id-max_part_number"
        """
        try:
            # Extract part numbers from display IDs
            part_numbers = []
            for display_id in display_ids:
                if '_p' in display_id:
                    part_num = int(display_id.split('_p')[1])
                    part_numbers.append(part_num)
            
            if not part_numbers:
                return display_ids[0] if display_ids else "unknown"
            
            # Generate combined ID
            base_id = display_ids[0]
            max_part = max(part_numbers)
            return f"{base_id}-{max_part}"
            
        except (ValueError, IndexError) as e:
            logger.warning(f"Failed to generate combined display ID: {e}")
            return display_ids[0] if display_ids else "unknown"