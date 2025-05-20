"""
Database integration for MongoDB to store reply data.
"""
import motor.motor_asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional

from app.config import MONGO_URL, MONGO_DB_NAME, REPLIES_COLLECTION


class Database:
    """MongoDB database handler for the application."""
    
    client = None
    db = None
    
    @classmethod
    async def connect(cls):
        """Establish connection to MongoDB."""
        if not cls.client:
            try:
                cls.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
                cls.db = cls.client[MONGO_DB_NAME]
                
                # Test connection by pinging the database
                await cls.client.admin.command('ping')
                print("Successfully connected to MongoDB")
                
                # Create indexes
                await cls.create_indexes()
                
            except Exception as e:
                print(f"Failed to connect to MongoDB: {e}")
                # We allow the API to start even if DB connection fails
                # In production, you might want to fail fast instead
    
    @classmethod
    async def close(cls):
        """Close the MongoDB connection."""
        if cls.client:
            cls.client.close()
            cls.client = None
            cls.db = None
            print("MongoDB connection closed")
    
    @classmethod
    async def create_indexes(cls):
        """Create necessary indexes for the replies collection."""
        if cls.db:
            await cls.db[REPLIES_COLLECTION].create_index("platform")
            await cls.db[REPLIES_COLLECTION].create_index("created_at")
            # Text index for searching in post_text and reply_text
            await cls.db[REPLIES_COLLECTION].create_index([
                ("post_text", "text"), 
                ("reply_text", "text")
            ])
    
    @classmethod
    async def store_reply(cls, reply_data: Dict[str, Any]) -> str:
        """
        Store a reply in the database.
        
        Args:
            reply_data: Dictionary containing reply data
            
        Returns:
            str: ID of the inserted document
        """
        if cls.db is None:  # Fix the check here
            await cls.connect()
            
        if cls.db is None:  # Ensure the connection is established
            print("Database connection unavailable, skipping storage")
            return None
            
        # Ensure we have a timestamp
        if 'created_at' not in reply_data:
            reply_data['created_at'] = datetime.now(datetime.timezone.utc)
            
        try:
            result = await cls.db[REPLIES_COLLECTION].insert_one(reply_data)
            print(f"Stored reply with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error storing reply: {e}")
            return None
    
    @classmethod
    async def get_recent_replies(
        cls, platform: Optional[str] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent replies, optionally filtered by platform.
        
        Args:
            platform: Optional platform to filter by
            limit: Maximum number of results
            
        Returns:
            List of reply documents
        """
        if cls.db is None:
            # await cls.connect()
            raise ValueError("Database connection is not initialized.")
        if cls.db is None:
            return []
            
        filter_query = {}
        if platform:
            filter_query["platform"] = platform
            
        try:
            cursor = cls.db[REPLIES_COLLECTION].find(filter_query) \
                .sort("created_at", -1) \
                .limit(limit)
            return await cursor.to_list(length=limit)
        except Exception as e:
            print(f"Error retrieving replies: {e}")
            return []