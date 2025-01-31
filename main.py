import asyncio
from telegram import Update, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
MINI_APP_URL = os.getenv('MINI_APP_URL', 'https://terabox-mini-app.onrender.com')
MONGODB_URI = os.getenv('MONGODB_URI')
ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS', '').split(','))) if os.getenv('ADMIN_IDS') else []

if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in environment variables")
if not MONGODB_URI:
    raise ValueError("No MONGODB_URI found in environment variables")

# MongoDB connection
try:
    client = MongoClient(MONGODB_URI)
    db = client.get_database('terabox_player')
    # Test connection
    client.server_info()
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message with a button that opens the webapp."""
    try:
        user_id = update.effective_user.id
        username = update.effective_user.username
        
        # Add user to database
        db.users.update_one(
            {'user_id': user_id},
            {
                '$set': {
                    'username': username,
                    'last_active': datetime.utcnow(),
                    'is_banned': False
                },
                '$setOnInsert': {
                    'joined_date': datetime.utcnow()
                }
            },
            upsert=True
        )
        
        button = KeyboardButton(
            text="🎬 Open Player",
            web_app=WebAppInfo(url=MINI_APP_URL)
        )
        keyboard = ReplyKeyboardMarkup(
            [[button]], 
            resize_keyboard=True
        )
        
        await update.message.reply_text(
            "Welcome to Terabox Player Bot! 🎥\n\n"
            "Click the button below to open the player:",
            reply_markup=keyboard
        )
        logger.info(f"Start command used by user {user_id}")
    except Exception as e:
        logger.error(f"Error in start command: {e}")
        await update.message.reply_text(
            "Sorry, something went wrong. Please try again later."
        )

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Terabox URLs sent to the bot."""
    try:
        url = update.message.text
        user_id = update.effective_user.id
        
        # Add URL to database
        video_data = {
            'user_id': user_id,
            'url': url,
            'added_date': datetime.utcnow(),
            'last_played': None,
            'play_count': 0
        }
        
        db.videos.insert_one(video_data)
        
        button = KeyboardButton(
            text="🎬 Open Player",
            web_app=WebAppInfo(url=MINI_APP_URL)
        )
        keyboard = ReplyKeyboardMarkup(
            [[button]], 
            resize_keyboard=True
        )
        
        await update.message.reply_text(
            "✅ Video added successfully!\n"
            "Click the button below to watch:",
            reply_markup=keyboard
        )
        logger.info(f"URL added by user {user_id}")
    except Exception as e:
        logger.error(f"Error handling URL: {e}")
        await update.message.reply_text(
            "Sorry, there was an error processing your URL."
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors in the bot."""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "Sorry, something went wrong. Please try again later."
        )

def main():
    """Start the bot."""
    try:
        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
        
        # Add error handler
        application.add_error_handler(error_handler)

        # Start the Bot
        logger.info("Starting bot...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == '__main__':
    main() 