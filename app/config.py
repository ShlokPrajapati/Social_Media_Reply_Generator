"""
Configuration settings for the social media reply generation system.
"""
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GOOGLE_API_KEY not set in environment variables")

# MongoDB configuration
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "social_media_replies")
REPLIES_COLLECTION = os.getenv("REPLIES_COLLECTION", "replies")

# API configuration
API_TITLE = "Social Media Reply Generator API"
API_DESCRIPTION = "API for generating human-like replies to social media posts"
API_VERSION = "0.1.0"

# Model configuration
MODEL_NAME = os.getenv("MODEL_NAME", "models/gemini-1.5-flash")
MODEL_TEMPERATURE = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
MODEL_MAX_OUTPUT_TOKENS = int(os.getenv("MODEL_MAX_OUTPUT_TOKENS", "500"))

# Platform configuration
SUPPORTED_PLATFORMS = ["twitter", "linkedin", "instagram", "facebook", "reddit"]

# Advanced settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"