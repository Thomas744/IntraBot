import logging
from pathlib import Path

LOG_FILE = Path(__file__).parent / "access_audit.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
)

def log_access(username, role, query, results_count):
    logging.info(
        f"user={username} role={role} query='{query}' results={results_count}"
    )
