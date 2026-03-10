# api/app/routers/genomics.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.models import Detection
from app.models.genomics import GenomicAnalysis, GenomeSearchResult
from app.services.ncbi_service import NCBIService
import uuid

router = APIRouter(prefix="/genomics", tags=["Genomics"])

@router.post("/analyze/{detection_id}")
async def analyze_detection(
    detection_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Start genom-analyse for en deteksjon"""
    detection = db.query(Detection).filter(Detection.detection_id == detection_id).first()
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    
    background_tasks.add_task(perform_genomic_search, detection_id, detection.object_class, db)
    return {"message": "Genomic analysis started", "detection_id": detection_id}

@router.get("/analysis/{analysis_id}")
def get_analysis(analysis_id: str, db: Session = Depends(get_db)):
    """Hent genom-analyse"""
    analysis = db.query(GenomicAnalysis).filter(GenomicAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis

@router.get("/detection/{detection_id}")
def get_analysis_by_detection(detection_id: int, db: Session = Depends(get_db)):
    """Hent analyse for en spesifikk deteksjon"""
    analysis = db.query(GenomicAnalysis).filter(
        GenomicAnalysis.detection_id == detection_id
    ).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="No analysis found for this detection")
    return analysis

async def perform_genomic_search(detection_id: int, object_class: str, db: Session):
    """Utfør genom-søk basert på deteksjon"""
    ncbi = NCBIService()
    
    # Opprett ny analyse
    analysis = GenomicAnalysis(
        id=uuid.uuid4(),
        detection_id=detection_id,
        species_prediction=object_class
    )
    db.add(analysis)
    db.commit()
    
    # Første søk - eksakt match
    results = await ncbi.search_genome(object_class)
    
    if not results:
        # Utvidet søk
        expanded_terms = await ncbi.expand_search(object_class)
        for term in expanded_terms:
            results = await ncbi.search_genome(term)
            if results:
                search_result = GenomeSearchResult(
                    id=uuid.uuid4(),
                    analysis_id=analysis.id,
                    genome_data=results,
                    search_parameters={"term": term, "expanded": True}
                )
                db.add(search_result)
                break
    
    if results:
        reports = results.get("reports", [])
        if reports:
            analysis.genome_accession = reports[0].get("accession")
            analysis.ncbi_taxonomy_id = str(reports[0].get("tax_id"))
            analysis.requires_human_review = False
    else:
        analysis.requires_human_review = True
        analysis.review_notes = "Ingen funn i NCBI-databaser"
    
    db.commit()