
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "memory_leak_simulator.db"

# Application-level safety limits
MAX_ITERATIONS = 100_000
MAX_DURATION_SECONDS = 30
MAX_MEMORY_MB = 200

DEFAULT_MEASUREMENT_INTERVAL = 5_000