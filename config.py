import os
from dotenv import load_dotenv

class Config:
    """Configuration class for the bot."""
    
    def __init__(self):
        load_dotenv()
        
        # Bot Configuration
        self.BOT_TOKEN = self._get_required('BOT_TOKEN')
        self.ADMIN_IDS = self._parse_admin_ids()
        
        # Mini App Configuration
        self.MINI_APP_URL = os.getenv('MINI_APP_URL', 'https://terabox-mini-app.onrender.com')
        
        # Database Configuration
        self.MONGODB_URI = self._get_required('MONGODB_URI')
        
        # API Configuration
        self.API_BASE = os.getenv('API_BASE', 'https://opabhik.serv00.net/Watch.php?url=')
        
        # Security
        self.ALLOWED_DOMAINS = ['terabox.com', '1024terabox.com']
    
    def _get_required(self, name: str) -> str:
        """Get a required environment variable."""
        value = os.getenv(name)
        if not value:
            raise ValueError(f"Missing required environment variable: {name}")
        return value
    
    def _parse_admin_ids(self) -> list:
        """Parse admin IDs from environment variable."""
        admin_ids = os.getenv('ADMIN_IDS', '')
        if not admin_ids:
            return []
        try:
            return [int(id.strip()) for id in admin_ids.split(',')]
        except ValueError:
            raise ValueError("Invalid ADMIN_IDS format. Must be comma-separated integers.") 