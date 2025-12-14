from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]

@dataclass(frozen=True)
class Paths:
    data_raw: Path = BASE_DIR / "data" / "raw"
    data_processed: Path = BASE_DIR / "data" / "processed"
    data_snapshots: Path = BASE_DIR / "data" / "snapshots"
    reports_daily: Path = BASE_DIR / "reports" / "daily"

def getenv(key: str, default: str | None = None) -> str | None:
    return os.getenv(key, default)

PATHS = Paths()
