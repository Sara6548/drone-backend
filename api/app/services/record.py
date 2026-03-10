import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.record import Record

def create_record(db: Session, payload: dict, file_path: str | None) -> Record:
    rec = Record(
        id=str(uuid.uuid4()),
        received_at=datetime.now(timezone.utc),
        file_path=file_path,
        payload=payload,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec