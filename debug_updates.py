import os
import sys
import httpx
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import asyncio

# Load from backend root and frontend root if needed
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
load_dotenv(os.path.join(os.path.dirname(__file__), "aimforge-app", ".env"))

print("--- DIAGNOSTIC REPORT ---")

gnews_key = os.getenv("GNEWS_API_KEY")
youtube_key = os.getenv("YOUTUBE_API_KEY")

print(f"GNEWS API KEY: {'CONFIGURED' if gnews_key else 'MISSING'}")
print(f"YOUTUBE API KEY: {'CONFIGURED' if youtube_key else 'MISSING'}")

async def test_gnews():
    if not gnews_key:
        print("GNEWS API: FAIL (Missing Key)")
        return
    try:
        url = f"https://gnews.io/api/v4/search?q=BGMI&lang=en&max=5&apikey={gnews_key}"
        async with httpx.AsyncClient() as client:
            res = await client.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                print(f"GNEWS API: PASS (Result count: {len(data.get('articles', []))})")
            else:
                print(f"GNEWS API: FAIL (HTTP {res.status_code}: {res.text})")
    except Exception as e:
        print(f"GNEWS API: FAIL ({e})")

async def test_youtube():
    if not youtube_key:
        print("YOUTUBE API: FAIL (Missing Key)")
        return
    try:
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=UCxT6X2VevmHcw4dnh_PjA-g&maxResults=5&order=date&type=video&key={youtube_key}"
        async with httpx.AsyncClient() as client:
            res = await client.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                print(f"YOUTUBE API: PASS (Result count: {len(data.get('items', []))})")
            else:
                print(f"YOUTUBE API: FAIL (HTTP {res.status_code}: {res.text})")
    except Exception as e:
        print(f"YOUTUBE API: FAIL ({e})")

async def main():
    await test_gnews()
    await test_youtube()
    
    # Try the backend endpoint locally (it might need auth, but we can check if it exists)
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get("http://localhost:8000/api/v1/updates", timeout=5)
            print(f"BACKEND ENDPOINT HTTP STATUS: {res.status_code}")
    except Exception as e:
         print(f"BACKEND ENDPOINT: FAIL ({e})")

asyncio.run(main())
