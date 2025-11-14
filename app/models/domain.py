from pydantic import BaseModel
from typing import List, Dict, Any

class DomainRequest(BaseModel):
    urls: List[str]

class SimilarWebRequest(BaseModel):
    domains: List[str]

class SimilarWebUpdateRequest(BaseModel):
    domain: str
    data: Dict[str, Any]


