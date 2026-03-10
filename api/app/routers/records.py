import json
import os
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.record import Record
from app.services.record import create_record
from app.schemas.records import RecordOut

router = APIRouter()

STORAGE_DIR = Path(os.getenv("STORAGE_DIR", "/data"))
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
@router.get("/records", response_model=list[RecordOut])
def list_records(db: Session = Depends(get_db)):
    return db.query(Record).order_by(Record.received_at.desc()).limit(100).all()

@router.post("/ingest")
async def ingest(
    payload: str = Form(...),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    try:
        metadata = json.loads(payload)
        if not isinstance(metadata, dict):
            raise ValueError("payload must be a JSON object")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid payload JSON: {e}")

    saved_path = None
    if file is not None:
        ext = Path(file.filename or "").suffix or ".bin"
        from uuid import uuid4
        file_id = str(uuid4())
        target = STORAGE_DIR / f"{file_id}{ext}"

        with target.open("wb") as f:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)

        saved_path = f"/data/{target.name}"

    rec = create_record(db, metadata, saved_path)

    return {
        "id": rec.id,
        "received_at": rec.received_at.isoformat(),
        "file_path": rec.file_path,
        "metadata": rec.payload,
    }


@router.get("/records")
def list_records(db: Session = Depends(get_db)):
    rows = db.query(Record).order_by(Record.received_at.desc()).limit(100).all()
    return [
        {
            "id": r.id,
            "received_at": r.received_at.isoformat(),
            "file_path": r.file_path,
            "metadata": r.payload,
        }
        for r in rows
    ]


@router.get("/records/{record_id}")
def get_record(record_id: str, db: Session = Depends(get_db)):
    r = db.get(Record, record_id)
    if not r:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": r.id,
        "received_at": r.received_at.isoformat(),
        "file_path": r.file_path,
        "metadata": r.payload,
    }
