import os
import requests
from dotenv import load_dotenv

load_dotenv()

SIMILARWEB_API_KEY = os.getenv("RAPIDAPI_KEY")
SIMILARWEB_API_HOST = os.getenv("SIMILARWEB_API_HOST", "similarweb-traffic.p.rapidapi.com")


def get_similarweb_data(domain: str):
    """
    Fetch traffic and engagement data from SimilarWeb API
    """
    url = "https://similarweb-traffic.p.rapidapi.com/traffic"
    querystring = {"domain": domain}
    
    headers = {
        "x-rapidapi-host": SIMILARWEB_API_HOST,
        "x-rapidapi-key": SIMILARWEB_API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"SimilarWeb API request failed: {str(e)}")
