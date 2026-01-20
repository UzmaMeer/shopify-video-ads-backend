from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

# Import Config and Routes
from config import VIDEO_DIR, BASE_PUBLIC_URL
from routes import video, auth, publish, general

app = FastAPI()

# --- Middleware ---
# 🟢 UPDATE: This list tells AWS who is allowed to connect
origins = [
    "http://localhost:3000",                     # Local React
    "https://shopify-video-ads.web.app",         # 🟢 YOUR LIVE FIREBASE SITE
    "https://shopify-video-ads.firebaseapp.com", # Alternative Firebase Domain
    "https://shopify-ext.20thletter.com",        # Your AWS Domain
    BASE_PUBLIC_URL                              # Dynamic URL
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, 
    allow_methods=["*"], 
    allow_headers=["*"], 
    allow_credentials=True
)

app.add_middleware(SessionMiddleware, secret_key="UZMA_VIDEO_PROJECT_FINAL_SECRET_999", same_site="lax", https_only=True)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# --- Mount Static Files ---
app.mount("/static", StaticFiles(directory=VIDEO_DIR), name="static")

# --- Include Routers ---
app.include_router(video.router)
app.include_router(auth.router)
app.include_router(publish.router)
app.include_router(general.router)

# --- Root Endpoint ---
@app.get("/")
def home(): 
    return RedirectResponse("https://shopify-video-ads.web.app")