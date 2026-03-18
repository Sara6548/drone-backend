# api/app/services/ncbi_service.py
import aiohttp
from typing import Optional, Dict, List
from app.core.config import NCBI_API_KEY

class NCBIService:
    BASE_URL = "https://api.ncbi.nlm.nih.gov/datasets/v2"
    
    def __init__(self):
        self.api_key = NCBI_API_KEY
        
    async def search_genome(self, species: str) -> Optional[Dict]:
        """Søk etter genom i NCBI"""
        async with aiohttp.ClientSession() as session:
            params = {"taxon": species, "limit": 10}
            if self.api_key:
                params["api_key"] = self.api_key
                
            url = f"{self.BASE_URL}/genome/taxon/{species}/dataset_report"
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    return await resp.json()
                return None
    
    async def expand_search(self, query: str) -> List[str]:
        """Utvid søk til relaterte termer"""
        expanded_terms = {
            "blad. epletre.": ["malus", "rosaceae", "leaf", "plant"],
            "blad. eik.": ["quercus", "fagaceae", "leaf"],
            "sopp.": ["fungi", "mushroom", "basidiomycota"],
        }
        return expanded_terms.get(query.lower(), [query])
    
    