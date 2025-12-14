"""Fetch SPY (price & volume) data.
MVP: implement later (e.g., yfinance/stooq)"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from mm.utils.db import get_con, ensure_raw_tables

def fetch_spy_data() -> pd.DataFrame:
    """
    fetch spy_data for the last 10 years (daily)
    """
    end = datetime.today()
    start = end - timedelta(days=10*365)

    df = yf.download(
        "SPY",
        start=start.strftime("%Y-%m-%d"),
        end=end.strftime("%Y-%m-%d"),
        auto_adjust=False,
        progress=False
    )

    # MultiIndex 컬럼이면 (Open, SPY) 같은 튜플 → Open만 남김
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()

    # date, open, high... 형태로 표준화
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]

    # adj_close 컬럼이 없으면 close로 대체
    if "adj_close" not in df.columns:
        df["adj_close"] = df["close"]

    return df

def upsert_spy_to_duckdb(df: pd.DataFrame) -> int:
    # 필요한 컬럼만 정리 + 타입 정리
    df = df.copy()
    df["symbol"] = "SPY"
    df["source"] = "yfiance"
    df["ingested_at"] = pd.Timestamp.utcnow()

    # date 컬럼 보장
    df["date"] = pd.to_datetime(df["date"]).dt.date

    cols = ["symbol", "date", "open", "high", "low", "close", "adj_close", "volume", "source", "ingested_at"]
    df = df[cols]

    con = get_con()
    try:
        ensure_raw_tables(con)

        # UPSERT: 같은 (symbol, date) 있으면 갱신
        con.register("tmp", df)
        con.execute("""
        INSERT INTO raw_prices_daily
        SELECT * FROM tmp
        ON CONFLICT(symbol, date) DO UPDATE SET
            open=excluded.open,
            high=excluded.high,
            low=excluded.low,
            close=excluded.close,
            adj_close=excluded.adj_close,
            volume=excluded.volume,
            source=excluded.source,
            ingested_at=excluded.ingested_at
        """)
        con.unregister("tmp")

        # 적재 row 수(대략) 확인용
        n = len(df)
        return n
    finally:
        con.close()

def main():
    print("[spy] fetch start")
    df = fetch_spy_data()
    print(f"[spy] fetched rows={len(df)} date_range={df['date'].min()}~{df['date'].max()}")

    n = upsert_spy_to_duckdb(df)
    print(f"[spy] upsert done rows={n}")

if __name__ == "__main__":
    main()

