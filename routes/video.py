import uuid
import json
import shutil
import os
import logging
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Form, File, UploadFile
from database import video_jobs_collection
from config import VIDEO_DIR

# 🟢 Import the task directly from tasks.py
from tasks import process_video_job_task 

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/api/start-video-generation")
async def start_gen(
    image_urls: str = Form(...), 
    product_title: str = Form(...), 
    product_desc: str = Form(...),
    logo_url: Optional[str] = Form(None), 
    voice_gender: str = Form("female"), 
    duration: int = Form(15),
    script_tone: str = Form("Professional"), 
    video_theme: str = Form("Modern"), 
    music_file: UploadFile = File(None),
    shop_name: str = Form(...)
):
    job_id = str(uuid.uuid4())
    logger.info(f"🚀 [BACKEND] Initiating video job {job_id} for store: {shop_name}")

    # 1. Save 'queued' status to MongoDB
    new_job = { 
        "job_id": job_id, 
        "status": "queued", 
        "progress": 0, 
        "created_at": datetime.utcnow(), 
        "shop_name": shop_name, 
        "title": product_title 
    }
    await video_jobs_collection.insert_one(new_job)

    # 2. Parse images
    try: 
        images_list = json.loads(image_urls)
    except Exception as e:
        logger.error(f"Failed to parse image URLs: {e}")
        images_list = []
    
    # 3. Handle Music
    custom_music_path = None
    if music_file:
        custom_music_path = os.path.join(VIDEO_DIR, f"bgm_{job_id}.mp3")
        with open(custom_music_path, "wb") as buffer:
            shutil.copyfileobj(music_file.file, buffer)
            
    # 4. 🟢 SEND TO CELERY
    try:
        # .delay() is the magic function that sends it to Redis
        process_video_job_task.delay(
            job_id, 
            images_list, 
            product_title, 
            product_desc, 
            logo_url, 
            voice_gender, 
            duration, 
            script_tone, 
            custom_music_path, 
            video_theme, 
            shop_name
        )
        logger.info(f"✅ [BACKEND] Job {job_id} sent to Celery!")
    except Exception as e:
        logger.error(f"❌ [BACKEND] Celery failed: {str(e)}")
        return {"status": "failed", "error": "Could not connect to Worker."}
    
    return {"status": "queued", "job_id": job_id}

@router.get("/api/check-status/{job_id}")
async def check_status(job_id: str):
    job = await video_jobs_collection.find_one({"job_id": job_id})
    if not job: return {"status": "not_found"}
    return { 
        "status": job.get("status"), 
        "progress": job.get("progress", 0), 
        "url": job.get("url"), 
        "error": job.get("error") 
    }