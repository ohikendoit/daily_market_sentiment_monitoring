import os
import duckdb

def get_con():
    db_path = os.getenv("DUCKDB_PATH", "data/market.duckdb")
    return duckdb.connect(database=db_path)

def ensure_raw_tables(conn: duckdb.DuckDBPyConnection):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS raw_prices_daily (
        symbol TEXT,
        date DATE,
        open DOUBLE,
        high DOUBLE,
        low DOUBLE,
        close DOUBLE,
        adj_close DOUBLE,
        volume BIGINT,
        source TEXT,
        ingested_at TIMESTAMP,
        PRIMARY KEY(symbol, date)
    );
    """)