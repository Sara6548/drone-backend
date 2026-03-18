from fastapi import APIRouter, Depends, HTTPException
from app.services.influxdb_client import InfluxDBService
from app.db.deps import get_db
from sqlalchemy.orm import Session
from app.models.models import Mission


router = APIRouter(prefix="/telemetry", tags=["Telemetry"])

@router.post("/drone/{drone_id}/sensor")
async def ingest_telemetry(
    drone_id: str,
    mission_id: int,
    sensor_type: str,
    value: float,
    unit: str,
    db: Session = Depends(get_db),
    influx: InfluxDBService = Depends(lambda: InfluxDBService())
):
    # Sjekk at mission eksisterer (PostgreSQL)
    mission = db.query(Mission).filter(Mission.mission_id == mission_id).first()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    
    # Skriv til InfluxDB (tidsserie)
    influx.write_sensor_data(drone_id, mission_id, sensor_type, value, unit)
    
    return {"status": "ok", "drone_id": drone_id}

@router.get("/drone/{drone_id}/history")
async def get_telemetry_history(
    drone_id: str,
    minutes: int = 10,
    influx: InfluxDBService = Depends(lambda: InfluxDBService())
):
    # Hent fra InfluxDB
    data = influx.query_recent_sensor_data(drone_id, minutes)
    
    # Formater resultatet
    result = []
    for table in data:
        for record in table.records:
            result.append({
                "time": record.get_time(),
                "sensor_type": record.values.get("sensor_type"),
                "value": record.get_value(),
                "unit": record.values.get("unit")
            })
    
    return result