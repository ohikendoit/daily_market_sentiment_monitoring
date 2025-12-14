from __future__ import annotations

from pathlib import Path

PROJECT_NAME = "market-monitoring"
PACKAGE_NAME = "mm"  # src/mm

DIRS = [
    "data/raw",
    "data/processed",
    "data/snapshots",
    "reports/daily",
    "reports/weekly",
    "reports/monthly",
    f"src/{PACKAGE_NAME}",
    f"src/{PACKAGE_NAME}/ingest",
    f"src/{PACKAGE_NAME}/indicators",
    f"src/{PACKAGE_NAME}/report",
    f"src/{PACKAGE_NAME}/alerts",
    f"src/{PACKAGE_NAME}/utils",
    "scripts",
    "tests",
]

FILES = {
    "README.md": f"""# {PROJECT_NAME}

MVP: U.S. market monitoring (S&P 500 / SPY, VIX, Fear & Greed, CPI, Forward P/E) with:
- daily/weekly/monthly changes
- basic technicals (RSI, Bollinger, volume vs 20D avg)
- stress-signal checks

## Quickstart
1) Create venv & install deps
2) Copy `.env.example` -> `.env` and fill keys (if needed)
3) Run:
   - `python scripts/run_daily.py`

## Output
- `reports/daily/` : rendered report (markdown/html/png)
- `data/snapshots/` : structured snapshot (csv/json)
""",
    ".env.example": """# Copy to .env (DO NOT COMMIT .env)
# Example:
# FRED_API_KEY=your_key
# DATA_PROVIDER=stooq|yfinance|custom
""",
    ".gitignore": """# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.so
*.egg-info/
.dist/
.build/
.venv/
venv/

# OS
.DS_Store
Thumbs.db

# Secrets
.env

# Outputs (keep if you want, adjust as needed)
data/raw/
data/processed/
reports/
""",
    f"src/{PACKAGE_NAME}/__init__.py": "",
    f"src/{PACKAGE_NAME}/config.py": """from __future__ import annotations
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
""",
    f"src/{PACKAGE_NAME}/ingest/__init__.py": "",
    f"src/{PACKAGE_NAME}/ingest/spy.py": """\"\"\"Fetch SPY (price & volume) data.
MVP: implement later (e.g., yfinance/stooq)\"\"\"
""",
    f"src/{PACKAGE_NAME}/ingest/vix.py": """\"\"\"Fetch VIX data.\"\"\"""",
    f"src/{PACKAGE_NAME}/ingest/fear_greed.py": """\"\"\"Fetch CNN Fear & Greed Index.\"\"\"""",
    f"src/{PACKAGE_NAME}/ingest/cpi.py": """\"\"\"Fetch U.S. CPI YoY (e.g., FRED CPIAUCSL YoY).\"\"\"""",
    f"src/{PACKAGE_NAME}/ingest/forward_pe.py": """\"\"\"Fetch S&P 500 forward P/E (source-dependent).\"\"\"""",
    f"src/{PACKAGE_NAME}/indicators/__init__.py": "",
    f"src/{PACKAGE_NAME}/indicators/returns.py": """\"\"\"Daily/weekly/monthly % changes utilities.\"\"\"""",
    f"src/{PACKAGE_NAME}/indicators/technicals.py": """\"\"\"RSI(14), Bollinger(20,2σ), volume vs 20D avg.\"\"\"""",
    f"src/{PACKAGE_NAME}/indicators/valuation.py": """\"\"\"Earnings yield (1/PE) and real earnings yield (EY - CPI YoY).\"\"\"""",
    f"src/{PACKAGE_NAME}/report/__init__.py": "",
    f"src/{PACKAGE_NAME}/report/table.py": """\"\"\"Build the unified KPI table with ↑/↓ formatting.\"\"\"""",
    f"src/{PACKAGE_NAME}/report/commentary.py": """\"\"\"Generate 1–2 sentence commentary (rule-based).\"\"\"""",
    f"src/{PACKAGE_NAME}/report/render.py": """\"\"\"Render markdown/html + save charts (png).\"\"\"""",
    f"src/{PACKAGE_NAME}/alerts/__init__.py": "",
    f"src/{PACKAGE_NAME}/alerts/stress.py": """\"\"\"Stress rules:
- S&P 500 daily move beyond ±1.5%
- VIX daily spike +10%
- Fear&Greed move beyond ±10 points
- RSI entering overbought/oversold
- SPY volume > +40% above 20D avg
\"\"\"""",
    f"src/{PACKAGE_NAME}/utils/__init__.py": "",
    f"src/{PACKAGE_NAME}/utils/dates.py": """\"\"\"Date helpers (US trading days vs calendar days).\"\"\"""",
    f"src/{PACKAGE_NAME}/utils/logging.py": """\"\"\"Logging helpers.\"\"\"""",
    "scripts/run_daily.py": """\"\"\"MVP runner (stub).
Later: fetch -> compute -> render -> save snapshot.
\"\"\"

def main() -> None:
    print("MVP scaffold ready. Next: implement data ingest + indicators + report rendering.")

if __name__ == "__main__":
    main()
""",
    "tests/test_smoke.py": """def test_smoke():
    assert True
""",
}

def ensure_dirs(base: Path) -> None:
    for d in DIRS:
        (base / d).mkdir(parents=True, exist_ok=True)

def ensure_files(base: Path) -> None:
    for rel, content in FILES.items():
        p = base / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if not p.exists():
            p.write_text(content, encoding="utf-8")

def main() -> None:
    base = Path.cwd()
    ensure_dirs(base)
    ensure_files(base)
    print("✅ MVP scaffold created/updated.")
    print(f"- package: src/{PACKAGE_NAME}")
    print("- next: implement ingest + indicators, then update scripts/run_daily.py")

if __name__ == "__main__":
    main()
