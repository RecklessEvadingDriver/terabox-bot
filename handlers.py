from telegram import Update, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import logging
from datetime import datetime
from .database import Database
from .utils import process_url, is_valid_terabox_url

logger = logging.getLogger(__name__)

class Handlers:
    def __init__(self, db: Database, config):
        self.db = db
        self.config = config

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        try:
            user_id = update.effective_user.id
            username = update.effective_user.username
            
            # Add user to database
            self.db.add_user(user_id, username)
            
            button = KeyboardButton(
                text="🎬 Open Player",
                web_app=WebAppInfo(url=self.config.MINI_APP_URL)
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

    async def handle_url(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle Terabox URLs."""
        try:
            url = update.message.text
            user_id = update.effective_user.id
            
            if not is_valid_terabox_url(url):
                await update.message.reply_text(
                    "❌ Please send a valid Terabox URL."
                )
                return
            
            processed_url = process_url(url, self.config.API_BASE)
            if not processed_url:
                await update.message.reply_text(
                    "❌ Failed to process video URL."
                )
                return
            
            # Add to database
            if not self.db.add_video(user_id, url, processed_url):
                await update.message.reply_text(
                    "❌ Failed to save video."
                )
                return
            
            button = KeyboardButton(
                text="🎬 Open Player",
                web_app=WebAppInfo(url=self.config.MINI_APP_URL)
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

    async def stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command."""
        try:
            if update.effective_user.id not in self.config.ADMIN_IDS:
                return
            
            stats = self.db.get_stats()
            await update.message.reply_text(
                f"📊 *Bot Statistics*\n\n"
                f"Total Users: `{stats.get('total_users', 0)}`\n"
                f"Active Today: `{stats.get('active_today', 0)}`\n"
                f"Total Videos: `{stats.get('total_videos', 0)}`",
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error in stats command: {e}")
            await update.message.reply_text(
                "Failed to get statistics."
            ) 