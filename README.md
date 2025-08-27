# XKCD Comic Crawler

A Python script to automatically download XKCD comic images from https://xkcd.com.

## Features

- Downloads comic images with proper filenames and metadata
- Respects rate limiting to avoid overwhelming the server
- Uses XKCD's official JSON API for reliable data extraction
- Supports downloading single comics or ranges
- Skips already downloaded comics
- Saves metadata (title, alt text, etc.) alongside images
- Robust error handling and retry logic

## Requirements

- Python 3.6+ (tested with Python 3.13)
- Internet connection

## Installation

1. Clone or download the script files:
```bash
git clone https://github.com/noskyzenx/xkcd-crawler.git
cd xkcd-crawler
```

2. Install the required Python packages:

```bash
pip3 install -r requirements.txt
```

Or install manually:
```bash
pip3 install requests beautifulsoup4
```

**Note**: Use `pip3` and `python3` commands for better compatibility across systems. Some systems may have `python` and `pip` commands available, but `python3` and `pip3` are more universally available.

## Usage

### Basic Usage

Download all XKCD comics (from 1 to latest):
```bash
python3 xkcd_crawler.py
```

### Download Options

Download comics 1-100:
```bash
python3 xkcd_crawler.py --start 1 --end 100
```

Download only the first 50 comics:
```bash
python3 xkcd_crawler.py --max 50
```

Download a single comic:
```bash
python3 xkcd_crawler.py --single 353
```

Specify custom output directory:
```bash
python3 xkcd_crawler.py --output /path/to/my/comics --start 1 --end 10
```

Adjust rate limiting (delay between requests):
```bash
python3 xkcd_crawler.py --delay 2.0 --start 1 --end 100
```

### Command Line Options

- `--start NUM`: Starting comic number (default: 1)
- `--end NUM`: Ending comic number (default: latest)
- `--max NUM`: Maximum number of comics to download
- `--single NUM`: Download a single comic by number
- `--output DIR`: Output directory (default: xkcd_images)
- `--delay SECONDS`: Delay between requests in seconds (default: 1.0)

## Output

The script creates an output directory (default: `xkcd_images`) containing:

- **Image files**: Named as `XXXX_Comic_Title.ext` (e.g., `0001_Barrel_-_Part_1.png`)
- **Metadata files**: JSON files with comic info (e.g., `0001_metadata.json`)

### Metadata Format

Each comic gets a metadata JSON file containing:
```json
{
  "comic_num": 1,
  "title": "Barrel - Part 1",
  "alt_text": "Don't we all.",
  "image_url": "https://imgs.xkcd.com/comics/barrel_cropped_(1).jpg",
  "filename": "0001_Barrel_-_Part_1.jpg"
}
```

## Examples

### Download first 10 comics with custom settings
```bash
python3 xkcd_crawler.py --start 1 --end 10 --output my_comics --delay 0.5
```

### Download specific range of comics
```bash
python3 xkcd_crawler.py --start 100 --end 200
```

### Download just one comic to test
```bash
python3 xkcd_crawler.py --single 1
```

## Notes

- The script respects XKCD's servers with rate limiting (1 second delay by default)
- Already downloaded comics are automatically skipped
- Comic #404 doesn't exist (XKCD joke), so it will be skipped
- Uses XKCD's official JSON API at `https://xkcd.com/{num}/info.0.json`
- Images are saved with original file extensions
- Progress is shown in the terminal

## Error Handling

- Network timeouts and connection errors are handled gracefully
- Missing comics (like #404) are skipped with a message
- Invalid comic numbers are handled appropriately
- Partial downloads can be resumed (already downloaded comics are skipped)

## Ethical Usage

This script is designed for educational and personal use. Please:
- Don't overwhelm XKCD's servers (use appropriate delays)
- Respect Randall Munroe's work and consider supporting XKCD
- Use downloaded content responsibly and in accordance with XKCD's license

## License

This script is provided as-is for educational purposes. XKCD comics are licensed under Creative Commons Attribution-NonCommercial 2.5 License.
