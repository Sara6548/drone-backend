# api/app/schemas/genomics.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

class GenomeSearchResultOut(BaseModel):
    id: UUID
    analysis_id: UUID
    ncbi_url: Optional[str] = None
    genome_data: Optional[Dict[str, Any]] = None
    search_parameters: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        orm_mode = True

class GenomicAnalysisOut(BaseModel):
    id: UUID
    detection_id: int
    sample_id: Optional[str] = None
    species_prediction: str
    confidence: Optional[float] = None
    genome_accession: Optional[str] = None
    ncbi_taxonomy_id: Optional[str] = None
    requires_human_review: bool
    review_notes: Optional[str] = None
    created_at: datetime
    search_results: list[GenomeSearchResultOut] = []
    
    class Config:
        orm_mode = True