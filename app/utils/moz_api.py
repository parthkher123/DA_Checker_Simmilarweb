
import requests
from fastapi import HTTPException
import logging
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

def get_domain_data_from_api(url: str):
    """Fetch DA/PA data from the RapidAPI service"""
    api_url = "https://moz-da-pa1.p.rapidapi.com/v1/getDaPa"
    rapidapi_key = os.getenv("RAPIDAPI_KEY")
    rapidapi_host = os.getenv("RAPIDAPI_HOST")
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": rapidapi_host,
        "x-rapidapi-key": rapidapi_key
    }
    payload = {"q": url}

    response = requests.post(api_url, json=payload, headers=headers)
    logger.info(f"🔍 Checking URL: {url}")
    logger.info(f"➡️  Status Code: {response.status_code}")
    logger.info(f"📦 Response: {response.text}")

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"API Error: {response.text}")

    try:
        data = response.json()
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid JSON response from API")

    da = data.get("domain_authority")
    pa = data.get("page_authority")

    logger.info(f"✅ Extracted DA: {da}, PA: {pa} for {url}")

    return {"url": url, "da": da, "pa": pa}
