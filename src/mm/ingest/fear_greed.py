"""Fetch CNN Fear & Greed Index."""

import pandas as pd
from datetime import datetime, timezone

import fear_and_greed

from mm.utils.db import get_con

TABLE = "raw_fear_greed_daily"
SOURCE = "fear-and-greed(pypi)"

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

def upsert_duckdb(metric_date, value, description, last_update_utc):
    con = get_con()
    try:
        ensure_table(con)

        ingested_at = datetime.now(timezone.utc)

        df = pd.DataFrame([{
            "metric_date": metric_date,
            "value": value,
            "description": description,
            "source_last_update_utc": last_update_utc,
            "ingested_at_utc": ingested_at,
            "source": SOURCE,
        }])

        con.register("tmp_fg", df)
        # DuckDB UPSERT (ON CONFLICT 지원 버전에 따라 문제 생길 수 있어 안전하게 MERGE로도 가능)
        con.execute(f"""
        INSERT INTO {TABLE}
        SELECT * FROM tmp_fg
        ON CONFLICT(metric_date) DO UPDATE SET
            value=excluded.value,
            description=excluded.description,
            source_last_update_utc=excluded.source_last_update_utc,
            ingested_at_utc=excluded.ingested_at_utc,
            source=excluded.source;
        """)
        con.unregister("tmp_fg")
    finally:
        con.close()

def main():
    try:
        fg = fear_and_greed.get()  # value, description
        # last_update는 timezone-aware UTC datetime이 들어오는 형태
        last_update_utc = fg.last_update.astimezone(timezone.utc)
        metric_date = last_update_utc.date()

        upsert_duckdb(
            metric_date=metric_date,
            value=float(fg.value),
            description=str(fg.description),
            last_update_utc=last_update_utc,
        )
        print(f"[fear_greed] upsert ok metric_date={metric_date} value={fg.value} desc={fg.description}")

    except Exception as e:
        # 운영에서는 로깅으로 남기고, 상위 레이어에서 N/A 처리하도록
        print(f"[fear_greed] failed: {e}")
        raise

if __name__ == "__main__":
    main()