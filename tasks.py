import os
import requests
import google.generativeai as genai
from pymongo import MongoClient
from datetime import datetime

# 🟢 CRITICAL IMPORT: This is the specific line you were missing!
# This tells tasks.py where to find the video generation logic.
from utils import generate_video_from_images 

# --- CONFIGURATION ---
# Database Connection
MONGO_DETAILS = "mongodb://localhost:27017"
client = MongoClient(MONGO_DETAILS)
db = client.video_ai_db
video_jobs_collection = db.get_collection("video_jobs")

# API Keys
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
BASE_PUBLIC_URL = "https://snakiest-edward-autochthonously.ngrok-free.dev"

# --- HELPER FUNCTIONS ---
def generate_viral_caption(title, desc):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = (f"Write a short, viral Instagram/TikTok caption for '{title}'. Include 3-4 trending hashtags. Under 2 sentences. No quotes.")
        resp = model.generate_content(prompt)
        return resp.text.strip()
    except:
        return f"Check out {title}! #Trending #Fashion"

# --- THE MAIN WORKER FUNCTION ---
def process_video_job_task(job_id, image_urls, title, desc, logo_url, voice_gender, duration, script_tone, custom_music_path, video_theme="Modern", shop_name=None):
    """
    Executes inside the Worker Process.
    """
    print(f"🛠️ Worker Starting Job: {job_id}")

    # 1. Helper to update DB progress
    def update_progress_db(percent):
        video_jobs_collection.update_one(
            {"job_id": job_id},
            {"$set": {"progress": percent, "status": "processing", "updated_at": datetime.utcnow()}}
        )

    try:
        # Initial DB Status
        update_progress_db(10)

        # 2. Call Utils to Generate Video
        # 🟢 This function call failed before because of the missing import above
        filename, script_used = generate_video_from_images(
            image_urls=image_urls, 
            product_title=title, 
            product_desc=desc, 
            logo_url=logo_url, 
            gender=voice_gender, 
            target_duration=duration, 
            script_tone=script_tone, 
            custom_music_path=custom_music_path, 
            progress_callback=update_progress_db,  # Pass DB updater
            shop_name=shop_name, 
            video_theme=video_theme
        )
        
        if filename:
            # 3. Update to 98% (Captioning Time)
            update_progress_db(98)
            
            # 4. Generate Caption
            smart_caption = generate_viral_caption(title, desc)
            
            # Construct URL
            video_url = f"{BASE_PUBLIC_URL}/static/{filename}"
            print(f"✅ Worker Finished: {filename}")
            
            # 5. Final Success Update in DB
            video_jobs_collection.update_one(
                {"job_id": job_id},
                {
                    "$set": {
                        "status": "done", 
                        "progress": 100, 
                        "url": video_url, 
                        "filename": filename, 
                        "caption": smart_caption,
                        "completed_at": datetime.utcnow()
                    }
                }
            )
        else:
            print(f"❌ Worker Failed: Utils returned None for {job_id}")
            video_jobs_collection.update_one(
                {"job_id": job_id},
                {"$set": {"status": "failed", "error": "Video generation returned no file."}}
            )

    except Exception as e:
        print(f"❌ Worker CRASH Error: {e}")
        video_jobs_collection.update_one(
            {"job_id": job_id},
            {"$set": {"status": "failed", "error": str(e)}}
        )