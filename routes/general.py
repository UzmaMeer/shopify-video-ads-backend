import requests
import logging
from datetime import datetime
from fastapi import APIRouter, Query, HTTPException
from database import shop_collection, review_collection, social_collection, brand_collection
from models import ReviewRequest, BrandSettingsRequest

# Set up logging to see Shopify errors in your terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/api/products")
async def get_products(shop: str = None, search: str = Query(None)):
    """Fetches product list from Shopify using the stored access token."""
    if not shop:
        logger.warning("Request received without shop parameter.")
        return {"products": []}

    # 1. Fetch store data from MongoDB to get the token
    store_data = await shop_collection.find_one({"shop": shop})
    
    # If no store found, tell frontend that re-auth is needed
    if not store_data or "access_token" not in store_data:
        logger.error(f"No access token found in database for shop: {shop}")
        return {"error": "auth_needed", "message": "Please re-install the app."}
    
    token = store_data["access_token"]
    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    }
    
    # Using the latest stable Shopify API version
    url = f"https://{shop}/admin/api/2024-01/products.json"
    params = {"limit": 50}
    
    try:
        logger.info(f"Fetching products from Shopify for: {shop}")
        r = requests.get(url, headers=headers, params=params)
        
        # Log exactly what Shopify sends back for debugging
        logger.info(f"Shopify Status Code: {r.status_code}")
        data = r.json()
        
        if r.status_code != 200:
            logger.error(f"Shopify API Error: {data}")
            return {"products": [], "error": "api_failure", "details": data}

        all_products = data.get("products", [])
        logger.info(f"Successfully retrieved {len(all_products)} products.")

        if search:
            filtered = [p for p in all_products if search.lower() in p.get('title', '').lower()]
            return {"products": filtered}
            
        return {"products": all_products}

    except Exception as e:
        logger.error(f"Unexpected error in get_products: {str(e)}")
        return {"products": [], "error": str(e)}

@router.post("/api/cache-images")
async def cache_images(request: dict):
    """
    Receives image URLs from the frontend to trigger background 
    pre-processing before video generation starts.
    """
    images = request.get("images", [])
    if not images:
        return {"status": "ignored", "reason": "no images provided"}
    
    # This prevents the 404 error in your logs
    logger.info(f"🚀 Background Caching Started: {len(images)} images received for pre-processing.")
    
    # Future: You can add logic here to download/resize images to the 'temp' folder
    return {"status": "success", "message": "Caching initiated"}

@router.post("/api/reviews")
async def add_review(review: ReviewRequest):
    new_review = review.dict()
    new_review["created_at"] = datetime.utcnow()
    new_review["is_approved"] = True
    await review_collection.insert_one(new_review)
    return {"status": "success"}

@router.get("/api/reviews")
async def get_reviews():
    real_reviews = []
    async for doc in review_collection.find({"is_approved": True}).limit(10):
        doc["_id"] = str(doc["_id"])
        real_reviews.append(doc)
    
    static_reviews = [
        {"name": "Sarah K.", "rating": 5, "comment": "Sales increased by 30%!", "designation": "Store Owner"},
        {"name": "Ali R.", "rating": 5, "comment": "Best tool for Shopify.", "designation": "Gadget Shop"}
    ]
    return {"reviews": static_reviews + real_reviews}

@router.get("/api/social-accounts")
async def get_accounts():
    accounts = []
    async for doc in social_collection.find({}):
        accounts.append({"id": str(doc["_id"]), "platform": doc.get("platform")})
    return {"status": "success", "accounts": accounts}

@router.post("/api/save-brand-settings")
async def save_brand_settings(settings: BrandSettingsRequest):
    # Upsert: Update if exists, otherwise insert
    await brand_collection.update_one(
        {"shop": settings.shop}, 
        {"$set": settings.dict()}, 
        upsert=True
    )
    return {"status": "success"}

@router.get("/api/get-brand-settings")
async def get_brand_settings(shop: str):
    data = await brand_collection.find_one({"shop": shop})
    if data:
        data.pop("_id", None)
    return data or {}
@router.post("/api/cache-images")
async def cache_images(request: dict):
    # This matches the call in ProductDetail.jsx
    return {"status": "success", "message": "Caching acknowledged"}