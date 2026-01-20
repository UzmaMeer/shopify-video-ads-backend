import os
# 🟢 ADD THESE TWO LINES
from dotenv import load_dotenv 
load_dotenv() 

import redis
from rq import Queue
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB Setup
# 🟢 Now this will actually read from your .env file!
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

# Redis Queue Setup
# 🟢 OPTIONAL: Make this dynamic too if you move to AWS later
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
redis_conn = redis.from_url(redis_url)
q = Queue(connection=redis_conn)