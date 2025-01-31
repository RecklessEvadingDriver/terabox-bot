import asyncio
import logging
from dotenv import load_dotenv
from .config import Config
from .bot import TeraboxBot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    """Main function to run the bot."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Initialize configuration
        config = Config()
        
        # Create and start bot
        bot = TeraboxBot(config)
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        raise
    finally:
        # Ensure bot is properly stopped
        if 'bot' in locals():
            await bot.stop()

if __name__ == "__main__":
    asyncio.run(main()) 