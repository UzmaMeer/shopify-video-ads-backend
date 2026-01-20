import os
from dotenv import load_dotenv

load_dotenv()

# Base Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(BASE_DIR, "video")
os.makedirs(VIDEO_DIR, exist_ok=True)

# 🟢 NOW IT IS DYNAMIC!
# It tries to get the link from .env. If missing, it falls back to your hardcoded Ngrok.
BASE_PUBLIC_URL = os.getenv("BASE_PUBLIC_URL", "https://snakiest-edward-autochthonously.ngrok-free.dev")

# API Keys
SHOPIFY_API_SECRET = os.getenv("SHOPIFY_API_SECRET")
META_CLIENT_ID = os.getenv("META_CLIENT_ID")
META_CLIENT_SECRET = os.getenv("META_CLIENT_SECRET")
IG_USER_ID = os.getenv("IG_USER_ID")
TIKTOK_CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
TIKTOK_CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")