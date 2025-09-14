#!/usr/bin/env python3
"""
Main entry point for bilibiliReuploader.

A tool for downloading Bilibili videos and re-uploading them to Internet Archive.
"""

import argparse
import sys
from typing import Optional

from config import Config
from logger import setup_logging
from app import ApplicationFactory


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Download Bilibili videos and re-upload to Internet Archive",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Run with default settings
  %(prog)s --streams-dir /path/to/streams --log-level DEBUG
  %(prog)s --max-retries 5 --retry-delay 60
        """
    )
    
    # Directory options
    parser.add_argument(
        '--streams-dir',
        default=None,
        help='Directory containing stream text files (default: from config/env)'
    )
    
    parser.add_argument(
        '--videos-dir', 
        default=None,
        help='Directory for downloaded videos (default: from config/env)'
    )
    
    # Processing options
    parser.add_argument(
        '--max-retries',
        type=int,
        default=None,
        help='Maximum number of retries for failed operations (default: from config/env)'
    )
    
    parser.add_argument(
        '--retry-delay',
        type=int,
        default=None,
        help='Delay in seconds between retries (default: from config/env)'
    )
    
    # Logging options
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Set the logging level (default: INFO)'
    )
    
    parser.add_argument(
        '--log-file',
        help='Log to file in addition to console'
    )
    
    # Other options
    parser.add_argument(
        '--ia-collection',
        default=None,
        help='Internet Archive collection name (default: from config/env)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 2.0.0'
    )
    
    return parser.parse_args()


def create_config_from_args(args: argparse.Namespace) -> Config:
    """Create configuration from command line arguments and environment."""
    # Start with environment/default config
    config = Config.from_env()
    
    # Override with command line arguments if provided
    if args.streams_dir is not None:
        config.streams_directory = args.streams_dir
    if args.videos_dir is not None:
        config.videos_directory = args.videos_dir
    if args.max_retries is not None:
        config.max_retries = args.max_retries
    if args.retry_delay is not None:
        config.retry_delay = args.retry_delay
    if args.ia_collection is not None:
        config.ia_collection = args.ia_collection
    
    return config


def main() -> int:
    """Main entry point."""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Set up logging
        logger = setup_logging(args.log_level, args.log_file)
        
        # Create configuration
        config = create_config_from_args(args)
        
        # Log configuration
        logger.info("Starting bilibiliReuploader with configuration:")
        logger.info(f"  Streams directory: {config.streams_directory}")
        logger.info(f"  Videos directory: {config.videos_directory}")
        logger.info(f"  Max retries: {config.max_retries}")
        logger.info(f"  Retry delay: {config.retry_delay}s")
        logger.info(f"  IA collection: {config.ia_collection}")
        
        # Create and run application
        app = ApplicationFactory.create_from_config(config)
        app.run()
        
        logger.info("Application completed successfully")
        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())