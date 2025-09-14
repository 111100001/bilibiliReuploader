# bilibiliReuploader

A tool for downloading Bilibili videos and re-uploading them to Internet Archive with proper metadata handling.

## Version 2.0 - Redesigned Architecture

This version represents a complete refactoring of the original script to follow best software design principles.

### Design Improvements

#### 1. **Single Responsibility Principle (SRP)**
- **Before**: One monolithic 265-line script handling all responsibilities
- **After**: Separate modules for distinct responsibilities:
  - `file_processor.py` - File operations and link extraction
  - `video_processor.py` - Video concatenation and FFmpeg operations
  - `json_processor.py` - JSON metadata handling
  - `download_manager.py` - Video downloads and Internet Archive uploads
  - `app.py` - Application orchestration

#### 2. **Separation of Concerns**
- **Configuration**: Centralized in `config.py` with environment variable support
- **Logging**: Proper logging framework in `logger.py` with configurable levels
- **CLI Interface**: Professional command-line interface in `main.py`
- **Error Handling**: Specific exception handling with retry mechanisms

#### 3. **Code Organization & Maintainability**
- **Modular Structure**: Easy to test, modify, and extend individual components
- **Type Hints**: Added throughout for better IDE support and code clarity
- **Documentation**: Comprehensive docstrings for all classes and methods
- **Constants**: Moved magic numbers to configuration
- **Clean Code**: Follows PEP 8 standards

#### 4. **Error Handling & Reliability**
- **Specific Exceptions**: Replace generic `Exception` handling
- **Retry Logic**: Exponential backoff instead of infinite loops
- **Logging**: Comprehensive logging for debugging and monitoring
- **Graceful Failures**: Proper cleanup and error reporting

#### 5. **Configuration Management**
- **Environment Variables**: Support for containerized deployments
- **CLI Arguments**: Override configuration via command line
- **Defaults**: Sensible defaults with easy customization

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd bilibiliReuploader

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

## Usage

### Basic Usage
```bash
python main.py
```

### Advanced Usage
```bash
# Custom directories and settings
python main.py --streams-dir /path/to/streams --max-retries 5 --log-level DEBUG

# Log to file
python main.py --log-file processing.log

# Custom Internet Archive collection
python main.py --ia-collection my-collection
```

### Environment Variables
```bash
export STREAMS_DIR=/path/to/streams
export VIDEOS_DIR=/path/to/videos
export MAX_RETRIES=10
export RETRY_DELAY=60
export IA_COLLECTION=my-collection
python main.py
```

## Architecture

### Class Diagram
```
BilibiliReuploader
├── FileProcessor (file operations)
├── VideoProcessor (video concatenation)
├── JsonProcessor (metadata handling)
├── DownloadManager (downloads/uploads)
└── RetryManager (error handling)
```

### Data Flow
1. **File Discovery**: Scan directory for text files containing video links
2. **Link Extraction**: Parse video URLs from text files
3. **Video Download**: Download videos using TubeUp/yt-dlp
4. **Concatenation**: Merge video parts using FFmpeg
5. **Metadata Processing**: Combine and format JSON metadata
6. **Upload**: Upload to Internet Archive with proper metadata
7. **Cleanup**: Optional cleanup of temporary files

## Configuration

### Default Configuration
```python
Config(
    streams_directory="/home/ubuntu/bilibiliReuploader/streams/failed",
    videos_directory="videos",
    last_processed_file="last_processed.txt",
    retry_delay=100,  # seconds
    max_retries=10,
    ffmpeg_loglevel="error",
    ia_collection="supertfLostMedia"
)
```

### Environment Override
All configuration can be overridden via environment variables with the `_` prefix:
- `STREAMS_DIR`
- `VIDEOS_DIR` 
- `LAST_PROCESSED_FILE`
- `RETRY_DELAY`
- `MAX_RETRIES`
- `FFMPEG_LOGLEVEL`
- `IA_COLLECTION`

## Dependencies

- `tubeup` - Video downloading and Internet Archive integration
- `yt-dlp` - Video downloading backend
- `internetarchive` - Internet Archive client
- `ffmpeg-python` - Video processing
- `bilibili-api-python` - Bilibili API access (for utilities)

## Migration from v1.0

The new version is backward compatible in terms of functionality but uses a completely different internal structure:

### Key Changes
1. **Entry Point**: Use `python main.py` instead of `python reuplod.py`
2. **Configuration**: Environment variables and CLI args instead of hardcoded values
3. **Logging**: Structured logging instead of print statements
4. **Error Handling**: Graceful error handling with retries

### Migrating
1. Update your scripts to call `python main.py`
2. Set environment variables for any custom paths
3. The original `reuplod.py` is preserved for reference

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Quality
```bash
# Check syntax
python -m py_compile *.py

# Format code
black .

# Type checking
mypy .
```

## Design Principles Applied

### SOLID Principles
- ✅ **Single Responsibility**: Each class has one clear purpose
- ✅ **Open/Closed**: Easy to extend without modifying existing code
- ✅ **Liskov Substitution**: Proper inheritance hierarchies
- ✅ **Interface Segregation**: Clean, focused interfaces
- ✅ **Dependency Inversion**: Depend on abstractions, not concretions

### Additional Principles
- ✅ **DRY (Don't Repeat Yourself)**: Common functionality extracted to utilities
- ✅ **KISS (Keep It Simple, Stupid)**: Simple, clear implementations
- ✅ **YAGNI (You Aren't Gonna Need It)**: No over-engineering
- ✅ **Separation of Concerns**: Clear boundaries between modules
- ✅ **Configuration Management**: Externalized configuration
- ✅ **Error Handling**: Comprehensive error handling strategies

## License

This project maintains the same license as the original codebase.