import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)
from .config import Config
from .database import Database
from .handlers import Handlers

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TeraboxBot:
    def __init__(self, config: Config):
        """Initialize bot with configuration."""
        self.config = config
        self.db = Database(config.MONGODB_URI)
        self.handlers = Handlers(self.db, config)
        
        # Initialize bot application
        self.app = Application.builder().token(config.BOT_TOKEN).build()
        self._setup_handlers()
        
        logger.info("Bot initialized successfully")
    
    def _setup_handlers(self):
        """Set up bot command and message handlers."""
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.handlers.start))
        self.app.add_handler(CommandHandler("stats", self.handlers.stats))
        
        # URL handler
        self.app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                self.handlers.handle_url
            )
        )
        
        logger.info("Bot handlers set up successfully")
    
    async def start(self):
        """Start the bot."""
        try:
            await self.app.initialize()
            await self.app.start()
            await self.app.run_polling()
            
            logger.info("Bot started successfully")
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise
    
    async def stop(self):
        """Stop the bot."""
        try:
            await self.app.stop()
            logger.info("Bot stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")
            raise 