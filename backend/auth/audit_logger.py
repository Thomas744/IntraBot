import logging
from pathlib import Path
import os

DATA_DIR = Path(os.getenv("DATA_DIR", "backend/auth"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = DATA_DIR / "access_audit.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
)

def log_access(username, role, query, results_count):
    logging.info(
        f"user={username} role={role} query='{query}' results={results_count}"
    )
