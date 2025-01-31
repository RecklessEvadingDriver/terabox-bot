import re
import requests
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

def is_valid_terabox_url(url: str) -> bool:
    """Check if URL is a valid Terabox URL."""
    try:
        parsed = urlparse(url)
        return (
            parsed.scheme in ['http', 'https'] and
            parsed.netloc in ['terabox.com', 'www.terabox.com']
        )
    except Exception as e:
        logger.error(f"Error validating URL: {e}")
        return False

def process_url(url: str, api_base: str) -> str:
    """Process Terabox URL to get direct stream URL."""
    try:
        # Extract video ID from URL
        match = re.search(r'/s/([A-Za-z0-9_-]+)', url)
        if not match:
            logger.error("Invalid Terabox URL format")
            return None
        
        video_id = match.group(1)
        
        # Call API to get direct stream URL
        response = requests.get(
            f"{api_base}/process",
            params={"url": url},
            timeout=10
        )
        
        if response.status_code != 200:
            logger.error(f"API error: {response.status_code}")
            return None
            
        data = response.json()
        if not data.get("success"):
            logger.error(f"API processing failed: {data.get('error')}")
            return None
            
        return data.get("stream_url")
    except requests.RequestException as e:
        logger.error(f"Request error: {e}")
        return None
    except Exception as e:
        logger.error(f"Error processing URL: {e}")
        return None

def format_size(size_bytes: int) -> str:
    """Format bytes to human readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def format_duration(seconds: int) -> str:
    """Format seconds to HH:MM:SS."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}" 