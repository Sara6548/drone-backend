import os

DATABASE_URL = os.getenv("DATABASE_URL", "")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

STORAGE_DIR = os.getenv("STORAGE_DIR", "/data")

NCBI_API_KEY = os.getenv("NCBI_API_KEY", "")
CLEANUP_INTERVAL = int(os.getenv("CLEANUP_INTERVAL", "86400"))


# NYTT: InfluxDB konfigurasjon
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://influxdb:8086")
INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "my-super-secret-token")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "drone-system")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "drone-telemetry")