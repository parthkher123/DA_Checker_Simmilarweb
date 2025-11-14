from fastapi import APIRouter
import logging
from app.models.domain import DomainRequest, SimilarWebRequest, SimilarWebUpdateRequest
from app.db.database import get_from_db, save_to_db, get_similarweb_from_db, save_similarweb_to_db, update_similarweb_in_db
from app.utils.moz_api import get_domain_data_from_api
from app.utils.similarweb_api import get_similarweb_data

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/check_domains")
def check_domains(request: DomainRequest):
    """Main endpoint to check multiple domain DA/PA values"""
    results = []
    for url in request.urls:
        existing = get_from_db(url)
        if existing:
            logger.info(f"✅ Cached result found for {url}")
            results.append(existing)
            continue
        logger.info(f"🌐 Fetching from API for {url}")
        api_data = get_domain_data_from_api(url)
        save_to_db(api_data["url"], api_data["da"], api_data["pa"])
        api_data["cached"] = False
        results.append(api_data)
    logger.info(f"✅ Completed processing {len(results)} domains.")
    return {"count": len(results), "results": results}


@router.post("/check_domains/refresh")
def refresh_domains(request: DomainRequest):
    """
    Endpoint to force refresh DA/PA data from API
    Ignores cache, fetches latest data from API and updates database
    """
    results = []
    for url in request.urls:
        logger.info(f"🔄 Force refreshing DA/PA data for {url}")
        try:
            # Fetch latest data from API
            api_data = get_domain_data_from_api(url)
            
            # Update/save to database
            save_to_db(api_data["url"], api_data["da"], api_data["pa"])
            
            logger.info(f"✅ DA/PA data refreshed and updated for {url}")
            api_data["refreshed"] = True
            api_data["cached"] = False
            api_data["message"] = "Data fetched from API and updated in database"
            results.append(api_data)
        except Exception as e:
            logger.error(f"❌ Error refreshing DA/PA data for {url}: {str(e)}")
            results.append({
                "url": url,
                "error": str(e),
                "refreshed": False
            })
    
    logger.info(f"✅ Completed refreshing {len(results)} domains.")
    return {"count": len(results), "results": results}


@router.post("/similarweb")
def check_similarweb_traffic(request: SimilarWebRequest):
    """
    Endpoint to fetch SimilarWeb traffic data for multiple domains
    Returns cached data if available, otherwise fetches from API
    """
    results = []
    
    for domain in request.domains:
        # Check if we have cached data
        existing = get_similarweb_from_db(domain)
        if existing:
            logger.info(f"✅ Cached SimilarWeb result found for {domain}")
            results.append(existing)
            continue
        
        # Fetch from API
        logger.info(f"🌐 Fetching SimilarWeb data from API for {domain}")
        try:
            api_data = get_similarweb_data(domain)
            save_similarweb_to_db(domain, api_data)
            logger.info(f"✅ SimilarWeb data saved for {domain}")
            results.append({
                "domain": domain,
                "data": api_data,
                "cached": False
            })
        except Exception as e:
            logger.error(f"❌ Error fetching SimilarWeb data for {domain}: {str(e)}")
            results.append({
                "domain": domain,
                "error": str(e),
                "cached": False
            })
    
    logger.info(f"✅ Completed processing {len(results)} domains.")
    return {"count": len(results), "results": results}


@router.post("/similarweb/refresh")
def refresh_similarweb_traffic(request: SimilarWebRequest):
    """
    Endpoint to force refresh SimilarWeb data from API
    Ignores cache, fetches latest data from API and updates database
    """
    results = []
    
    for domain in request.domains:
        logger.info(f"🔄 Force refreshing SimilarWeb data for {domain}")
        try:
            # Fetch latest data from API
            api_data = get_similarweb_data(domain)
            
            # Update/save to database
            save_similarweb_to_db(domain, api_data)
            
            logger.info(f"✅ SimilarWeb data refreshed and updated for {domain}")
            results.append({
                "domain": domain,
                "data": api_data,
                "refreshed": True,
                "message": "Data fetched from API and updated in database"
            })
        except Exception as e:
            logger.error(f"❌ Error refreshing SimilarWeb data for {domain}: {str(e)}")
            results.append({
                "domain": domain,
                "error": str(e),
                "refreshed": False
            })
    
    logger.info(f"✅ Completed refreshing {len(results)} domains.")
    return {"count": len(results), "results": results}



