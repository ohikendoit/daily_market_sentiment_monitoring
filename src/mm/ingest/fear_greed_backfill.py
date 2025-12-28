"""
Backfill CNN Fear & Greed Index history via CNN internal graphdata endpoint.
Then upsert into DuckDB raw_fear_greed_daily.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests

from mm.utils.db import get_con

TABLE = "raw_fear_greed_daily"
SOURCE = "cnn-graphdata"

BASE_URL = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"

HEADERS = {
    # 일부 환경에서 418/차단 비슷한 문제가 나오는 케이스가 있어 UA를 넣는 게 안전
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome Safari"
}

def ensure_table(con):
    con.execute(f"""
    CREATE TABLE IF NOT EXISTS {TABLE} (
        metric_date DATE PRIMARY KEY,
        value DOUBLE,
        description TEXT,
        source_last_update_utc TIMESTAMP,
        ingested_at_utc TIMESTAMP,
        source TEXT
    );
    """)

def _to_utc_dt(ts: Any) -> Optional[datetime]:
    """
    CNN graphdata에는 보통 timestamp(ms) 또는 ISO-like string이 섞여 나올 수 있음.
    가장 흔한 케이스: epoch milliseconds.
    """
    if ts is None:
        return None
    if isinstance(ts, (int, float)):
        # epoch milliseconds 추정
        if ts > 10_000_000_000:  # ms
            return datetime.fromtimestamp(ts / 1000.0, tz=timezone.utc)
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    if isinstance(ts, str):
        # 예: "2025-12-28T00:00:00Z" 등인 경우
        try:
            return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)
        except Exception:
            return None
    return None

def fetch_graphdata(date_str: Optional[str] = None) -> Dict[str, Any]:
    """
    - 전체: BASE_URL
    - 특정일: BASE_URL/YYYY-MM-DD
    """
    url = BASE_URL if not date_str else f"{BASE_URL}/{date_str}"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()

def normalize_rows(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    payload에서 시계열을 뽑아 (metric_date, value, description, source_last_update_utc, ingested_at_utc, source)로 정규화.
    CNN 포맷은 바뀔 수 있으니, 가능한 범용적으로 처리.
    """
    ingested_at = datetime.now(timezone.utc)

    rows: List[Dict[str, Any]] = []

    # (케이스1) 많은 예제에서 historical이 이렇게 들어옴: payload["fear_and_greed_historical"]["data"]
    hist = None
    if isinstance(payload.get("fear_and_greed_historical"), dict):
        hist = payload["fear_and_greed_historical"].get("data")

    # (케이스2) 날짜 단일 조회일 때 payload["fear_and_greed"]에 오늘 값이 들어올 수 있음
    single = payload.get("fear_and_greed")

    if isinstance(hist, list) and len(hist) > 0:
        for x in hist:
            # 보통 x에 score/value, rating, timestamp 등이 있음
            score = x.get("score") if isinstance(x, dict) else None
            rating = x.get("rating") if isinstance(x, dict) else None
            ts = x.get("timestamp") if isinstance(x, dict) else None
            dt = _to_utc_dt(ts)
            if dt is None or score is None:
                continue
            rows.append({
                "metric_date": dt.date(),
                "value": float(score),
                "description": str(rating) if rating is not None else None,
                "source_last_update_utc": dt,
                "ingested_at_utc": ingested_at,
                "source": SOURCE,
            })

    elif isinstance(single, dict) and single.get("score") is not None:
        dt = _to_utc_dt(single.get("timestamp")) or ingested_at
        rows.append({
            "metric_date": dt.date(),
            "value": float(single.get("score")),
            "description": str(single.get("rating")) if single.get("rating") is not None else None,
            "source_last_update_utc": dt,
            "ingested_at_utc": ingested_at,
            "source": SOURCE,
        })

    return rows

def upsert_rows(rows: List[Dict[str, Any]]) -> int:
    if not rows:
        return 0
    con = get_con()
    try:
        ensure_table(con)
        n = 0
        for r in rows:
            con.execute(
                f"""
                INSERT INTO {TABLE}
                (metric_date, value, description, source_last_update_utc, ingested_at_utc, source)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(metric_date) DO UPDATE SET
                    value=excluded.value,
                    description=excluded.description,
                    source_last_update_utc=excluded.source_last_update_utc,
                    ingested_at_utc=excluded.ingested_at_utc,
                    source=excluded.source;
                """,
                [
                    r["metric_date"],
                    r["value"],
                    r["description"],
                    r["source_last_update_utc"],
                    r["ingested_at_utc"],
                    r["source"],
                ],
            )
            n += 1
        return n
    finally:
        con.close()

def main():
    # 전체 백필
    payload = fetch_graphdata()
    rows = normalize_rows(payload)
    n = upsert_rows(rows)
    if rows:
        print(f"[fear_greed_backfill] upserted={n} range={min(r['metric_date'] for r in rows)}~{max(r['metric_date'] for r in rows)}")
    else:
        print("[fear_greed_backfill] no rows parsed (endpoint format changed or blocked)")

if __name__ == "__main__":
    main()
