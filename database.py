from pymongo import MongoClient
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, mongodb_uri: str):
        """Initialize database connection."""
        try:
            self.client = MongoClient(mongodb_uri)
            self.db = self.client.terabox_bot
            self.users = self.db.users
            self.videos = self.db.videos
            
            # Create indexes
            self.users.create_index("user_id", unique=True)
            self.videos.create_index([("user_id", 1), ("original_url", 1)], unique=True)
            
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def add_user(self, user_id: int, username: str = None) -> bool:
        """Add or update user in database."""
        try:
            self.users.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "username": username,
                        "last_active": datetime.utcnow()
                    },
                    "$setOnInsert": {
                        "joined_at": datetime.utcnow()
                    }
                },
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Error adding user: {e}")
            return False

    def add_video(self, user_id: int, original_url: str, processed_url: str) -> bool:
        """Add video to database."""
        try:
            self.videos.update_one(
                {
                    "user_id": user_id,
                    "original_url": original_url
                },
                {
                    "$set": {
                        "processed_url": processed_url,
                        "updated_at": datetime.utcnow()
                    },
                    "$setOnInsert": {
                        "added_at": datetime.utcnow()
                    }
                },
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Error adding video: {e}")
            return False

    def get_user_videos(self, user_id: int) -> list:
        """Get all videos for a user."""
        try:
            return list(self.videos.find(
                {"user_id": user_id},
                {"_id": 0, "original_url": 1, "processed_url": 1, "added_at": 1}
            ).sort("added_at", -1))
        except Exception as e:
            logger.error(f"Error getting user videos: {e}")
            return []

    def get_stats(self) -> dict:
        """Get bot statistics."""
        try:
            today = datetime.utcnow().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            
            total_users = self.users.count_documents({})
            active_today = self.users.count_documents({
                "last_active": {"$gte": today}
            })
            total_videos = self.videos.count_documents({})
            
            return {
                "total_users": total_users,
                "active_today": active_today,
                "total_videos": total_videos
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {} 