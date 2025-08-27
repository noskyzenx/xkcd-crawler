#!/usr/bin/env python3
"""
XKCD Comic Crawler

This script crawls XKCD comics and downloads their images.
Usage: python3 xkcd_crawler.py [options]

Requires Python 3.6+
"""

import requests
import os
import time
import json
import argparse
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import sys

class XKCDCrawler:
    def __init__(self, output_dir="xkcd_images", delay=1.0):
        """
        Initialize the XKCD crawler.
        
        Args:
            output_dir (str): Directory to save images
            delay (float): Delay between requests in seconds
        """
        self.base_url = "https://xkcd.com"
        self.output_dir = Path(output_dir)
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'XKCD-Crawler/1.0 (Educational Purpose)'
        })
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
    def get_latest_comic_number(self):
        """Get the number of the latest XKCD comic."""
        try:
            response = self.session.get(f"{self.base_url}/info.0.json")
            response.raise_for_status()
            data = response.json()
            return data['num']
        except Exception as e:
            print(f"Error getting latest comic number: {e}")
            return None
    
    def get_comic_info(self, comic_num):
        """
        Get comic information using XKCD's JSON API.
        
        Args:
            comic_num (int): Comic number
            
        Returns:
            dict: Comic information or None if error
        """
        try:
            url = f"{self.base_url}/{comic_num}/info.0.json"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Comic {comic_num} not found (404)")
                return None
            else:
                print(f"HTTP error for comic {comic_num}: {e}")
                return None
        except Exception as e:
            print(f"Error getting comic {comic_num} info: {e}")
            return None
    
    def download_image(self, image_url, filename):
        """
        Download an image from URL.
        
        Args:
            image_url (str): URL of the image
            filename (str): Local filename to save as
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            response = self.session.get(image_url, stream=True)
            response.raise_for_status()
            
            filepath = self.output_dir / filename
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return True
        except Exception as e:
            print(f"Error downloading {image_url}: {e}")
            return False
    
    def crawl_comic(self, comic_num):
        """
        Crawl a single XKCD comic.
        
        Args:
            comic_num (int): Comic number to crawl
            
        Returns:
            dict: Result with success status and info
        """
        print(f"Crawling comic {comic_num}...")
        
        # Get comic info
        comic_info = self.get_comic_info(comic_num)
        if not comic_info:
            return {"success": False, "comic_num": comic_num, "error": "Could not fetch comic info"}
        
        # Extract image URL and other info
        image_url = comic_info.get('img')
        title = comic_info.get('safe_title', f"comic_{comic_num}")
        alt_text = comic_info.get('alt', '')
        
        if not image_url:
            return {"success": False, "comic_num": comic_num, "error": "No image URL found"}
        
        # Create filename
        parsed_url = urlparse(image_url)
        file_extension = os.path.splitext(parsed_url.path)[1] or '.png'
        filename = f"{comic_num:04d}_{title.replace(' ', '_').replace('/', '_')}{file_extension}"
        
        # Check if file already exists
        filepath = self.output_dir / filename
        if filepath.exists():
            print(f"  Image already exists: {filename}")
            return {
                "success": True, 
                "comic_num": comic_num, 
                "filename": filename,
                "title": title,
                "alt_text": alt_text,
                "skipped": True
            }
        
        # Download the image
        success = self.download_image(image_url, filename)
        
        if success:
            print(f"  Downloaded: {filename}")
            
            # Save metadata
            metadata = {
                "comic_num": comic_num,
                "title": title,
                "alt_text": alt_text,
                "image_url": image_url,
                "filename": filename
            }
            
            metadata_file = self.output_dir / f"{comic_num:04d}_metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            return {
                "success": True, 
                "comic_num": comic_num, 
                "filename": filename,
                "title": title,
                "alt_text": alt_text,
                "skipped": False
            }
        else:
            return {"success": False, "comic_num": comic_num, "error": "Failed to download image"}
    
    def crawl_range(self, start=1, end=None, max_comics=None):
        """
        Crawl a range of XKCD comics.
        
        Args:
            start (int): Starting comic number
            end (int): Ending comic number (None for latest)
            max_comics (int): Maximum number of comics to download
        """
        if end is None:
            latest = self.get_latest_comic_number()
            if latest is None:
                print("Could not determine latest comic number")
                return
            end = latest
        
        print(f"Starting crawl from comic {start} to {end}")
        print(f"Output directory: {self.output_dir.absolute()}")
        print(f"Rate limit delay: {self.delay} seconds")
        print()
        
        successful = 0
        failed = 0
        skipped = 0
        
        for comic_num in range(start, end + 1):
            if max_comics and successful >= max_comics:
                print(f"Reached maximum of {max_comics} comics downloaded.")
                break
                
            result = self.crawl_comic(comic_num)
            
            if result["success"]:
                if result.get("skipped"):
                    skipped += 1
                else:
                    successful += 1
            else:
                failed += 1
                print(f"  Failed: {result.get('error', 'Unknown error')}")
            
            # Rate limiting
            if comic_num < end:
                time.sleep(self.delay)
        
        print(f"\nCrawling completed!")
        print(f"Successfully downloaded: {successful}")
        print(f"Skipped (already existed): {skipped}")
        print(f"Failed: {failed}")


def main():
    parser = argparse.ArgumentParser(description="Crawl XKCD comics and download images")
    parser.add_argument("--start", type=int, default=1, 
                       help="Starting comic number (default: 1)")
    parser.add_argument("--end", type=int, default=None, 
                       help="Ending comic number (default: latest)")
    parser.add_argument("--max", type=int, default=None, 
                       help="Maximum number of comics to download")
    parser.add_argument("--output", type=str, default="xkcd_images", 
                       help="Output directory (default: xkcd_images)")
    parser.add_argument("--delay", type=float, default=1.0, 
                       help="Delay between requests in seconds (default: 1.0)")
    parser.add_argument("--single", type=int, default=None,
                       help="Download a single comic by number")
    
    args = parser.parse_args()
    
    crawler = XKCDCrawler(output_dir=args.output, delay=args.delay)
    
    if args.single:
        # Download single comic
        result = crawler.crawl_comic(args.single)
        if result["success"]:
            print("Single comic downloaded successfully!")
        else:
            print(f"Failed to download comic {args.single}: {result.get('error')}")
    else:
        # Download range of comics
        crawler.crawl_range(start=args.start, end=args.end, max_comics=args.max)


if __name__ == "__main__":
    main()
