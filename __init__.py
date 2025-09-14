"""
bilibiliReuploader - A tool for downloading Bilibili videos and re-uploading to Internet Archive.

This package provides a modular, well-structured approach to processing Bilibili video files
and uploading them to the Internet Archive with proper metadata handling.
"""

__version__ = "2.0.0"
__author__ = "bilibiliReuploader Contributors"
__description__ = "Download Bilibili videos and re-upload to Internet Archive"

from .app import BilibiliReuploader, ApplicationFactory
from .config import Config

__all__ = [
    "BilibiliReuploader",
    "ApplicationFactory", 
    "Config",
]