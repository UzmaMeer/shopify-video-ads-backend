import os
from dotenv import load_dotenv 
load_dotenv() 

from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB Setup
MONGO_DETAILS = os.getenv("MONGO_DETAILS") 

client_db = AsyncIOMotorClient(MONGO_DETAILS)
database = client_db.video_ai_db

# Collections
video_jobs_collection = database.get_collection("video_jobs")
social_collection = database.get_collection("social_accounts")
shop_collection = database.get_collection("shopify_stores")
brand_collection = database.get_collection("brand_settings")
publish_collection = database.get_collection("publish_jobs")
review_collection = database.get_collection("user_reviews")

