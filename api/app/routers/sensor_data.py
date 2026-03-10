from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.models.models import Mission, SensorData
from app.schemas.schemas import SensorDataCreate, SensorDataOut

router = APIRouter(prefix="/missions/{mission_id}/sensor-data", tags=["Sensor Data"])


def _get_mission_or_404(mission_id: int, db: Session) -> Mission:
    mission = db.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


@router.post("", response_model=SensorDataOut, status_code=201)
def add_sensor_data(mission_id: int, body: SensorDataCreate, db: Session = Depends(get_db)):
    _get_mission_or_404(mission_id, db)
    reading = SensorData(mission_id=mission_id, **body.model_dump())
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading


@router.get("", response_model=list[SensorDataOut])
def list_sensor_data(mission_id: int, db: Session = Depends(get_db)):
    _get_mission_or_404(mission_id, db)
    return (
        db.query(SensorData)
        .filter(SensorData.mission_id == mission_id)
        .order_by(SensorData.timestamp.desc())
        .all()
    )


@router.get("/latest", response_model=SensorDataOut)
def latest_sensor_data(mission_id: int, db: Session = Depends(get_db)):
    _get_mission_or_404(mission_id, db)
    reading = (
        db.query(SensorData)
        .filter(SensorData.mission_id == mission_id)
        .order_by(SensorData.timestamp.desc())
        .first()
    )
    if not reading:
        raise HTTPException(status_code=404, detail="No sensor data for this mission")
    return reading