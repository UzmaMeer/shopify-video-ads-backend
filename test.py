import os
from dotenv import load_dotenv
from pymongo import MongoClient

# 1. Load Environment Variables
load_dotenv()

# 2. Get the Link
mongo_link = os.getenv("MONGO_DETAILS")

print("🔍 DIAGNOSTICS:")
print(f"   1. Mongo Link Found? {'✅ YES' if mongo_link else '❌ NO'}")

if mongo_link:
    print(f"   2. Link starts with: {mongo_link[:15]}...") 
    
    # 3. Try Connecting
    try:
        client = MongoClient(mongo_link)
        db = client.video_ai_db
        count = db.video_jobs.count_documents({})
        print(f"   3. Connection Success! Found {count} jobs in Cloud DB.")
        
        # 4. Send a Test Signal
        db.video_jobs.insert_one({"test": "Hello from Python", "status": "debug_test"})
        print("   4. ✅ Sent a 'Test Document' to Atlas. Check your browser now!")
    except Exception as e:
        print(f"   ❌ Connection Failed: {str(e)}")
else:
    print("   ❌ ERROR: Python cannot find 'MONGO_DETAILS' in your .env file.")
    print("      Make sure you saved the .env file!")