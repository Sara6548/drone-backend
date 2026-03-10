# api/app/models/genomics.py
from sqlalchemy import Column, BigInteger, String, Text, Enum, TIMESTAMP, DECIMAL, ForeignKey, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
import uuid

class GenomicAnalysis(Base):
    __tablename__ = "genomic_analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    detection_id = Column(BigInteger, ForeignKey("detections.detection_id", ondelete="CASCADE"))
    sample_id = Column(String(100), unique=True, nullable=True)
    species_prediction = Column(String(200))
    confidence = Column(DECIMAL(5, 4), nullable=True)
    genome_accession = Column(String(50), nullable=True)
    ncbi_taxonomy_id = Column(String(20), nullable=True)
    requires_human_review = Column(Boolean, default=False)
    review_notes = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    detection = relationship("Detection", back_populates="genomic_data")
    search_results = relationship("GenomeSearchResult", back_populates="analysis", cascade="all, delete-orphan")

class GenomeSearchResult(Base):
    __tablename__ = "genome_search_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("genomic_analyses.id", ondelete="CASCADE"))
    ncbi_url = Column(String(500), nullable=True)
    genome_data = Column(JSONB, nullable=True)
    search_parameters = Column(JSONB, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    analysis = relationship("GenomicAnalysis", back_populates="search_results")
    
    