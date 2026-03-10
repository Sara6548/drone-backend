## Drone Backend – V1

### Start
docker compose up -d --build

### Health
GET /health

### Ingest data
POST /ingest (multipart/form-data)

payload: JSON string
file: optional image

### Database
Table: records
- id
- received_at
- file_path
- metadata (JSONB)
