import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Load the .env file
print("📂 Loading .env file...")
loaded = load_dotenv()

if not loaded:
    print("❌ ERROR: Could not find or load .env file!")
    print("   -> Make sure you created a file named '.env' (no name, just extension)")
    exit()

# 2. Check if Variables exist (Without printing them completely)
gemini_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_PUBLIC_URL")

print(f"✅ .env Loaded Successfully!")
print(f"   - BASE_PUBLIC_URL: {base_url if base_url else '❌ MISSING'}")
print(f"   - GEMINI_API_KEY:  {'✅ Found' if gemini_key else '❌ MISSING'}")

# 3. Test the Key with a real Request
if gemini_key:
    print("\n🤖 Testing Gemini API connection...")
    try:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Say 'Hello from AI' if you can hear me.")
        
        print(f"🎉 SUCCESS! API Response: {response.text.strip()}")
    except Exception as e:
        print(f"❌ API KEY FAILED: {str(e)}")
else:
    print("❌ Cannot test API because the key is missing from .env")