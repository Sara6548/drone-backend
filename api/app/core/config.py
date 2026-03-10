import os

DATABASE_URL = os.getenv("DATABASE_URL", "")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

STORAGE_DIR = os.getenv("STORAGE_DIR", "/data")

NCBI_API_KEY = os.getenv("NCBI_API_KEY", "")
CLEANUP_INTERVAL = int(os.getenv("CLEANUP_INTERVAL", "86400"))