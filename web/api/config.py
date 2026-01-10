from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = Path(__file__).parent.parent / "drills.db"

# Exercise topics to scan
TOPICS = ["sorting", "graphs", "trees"]

# Code execution settings
CODE_TIMEOUT = 10  # seconds
MAX_CODE_SIZE = 50_000  # bytes

# Security settings
ALLOWED_PATH_CHARS = set("abcdefghijklmnopqrstuvwxyz0123456789_")
