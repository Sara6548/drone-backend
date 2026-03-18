from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.telemetry import router as telemetry_router
from app.routers.missions import router as missions_router
from app.routers.sensor_data import router as sensor_data_router
from app.routers.detections import router as detections_router
from app.routers import genomics # ny import


app = FastAPI(
    title="Drone Backend API",
    description="Mission management and telemetry ingestion for drone operations.",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(missions_router)
app.include_router(sensor_data_router)
app.include_router(detections_router)
app.include_router(genomics.router) # ny router
app.include_router(telemetry_router)
