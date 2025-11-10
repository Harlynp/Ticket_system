# config.py
"""
Central configuration using environment variables with safe defaults.
"""
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.resolve()

# Paths – override with env vars
DATA_DIR = Path(os.getenv("TICKET_DATA_DIR", BASE_DIR / "data"))
LOG_DIR = Path(os.getenv("TICKET_LOG_DIR", BASE_DIR / "Log Files"))

TICKETS_FILE = DATA_DIR / "tickets.json"
COUNTER_FILE = DATA_DIR / "counter.txt"

# Validation rules
MAX_DESCRIPTION_LENGTH = 500
MAX_USERNAME_LENGTH = 50
USERNAME_REGEX = r"^[a-zA-Z0-9.]+$"

# App constants
DEFAULT_COUNTER = 1000
DATE_FORMAT = "%d/%m/%Y"