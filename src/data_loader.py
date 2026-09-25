"""ThreatLens — load network logs into pandas + SQLite."""

import pandas as pd
from pathlib import Path
from src.database.database import get_connection, init_db


REQUIRED_COLUMNS = {
    "timestamp", "source_ip", "destination_ip", "source_port",
    "destination_port", "protocol", "packet_count", "packet_size",
    "bytes_transferred", "connection_duration", "status",
}


def validate_schema(df: pd.DataFrame) -> tuple[bool, str]:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        return False, f"Missing columns: {', '.join(sorted(missing))}"
    if df.empty:
        return False, "Dataset is empty."
    return True, "OK"


def load_csv(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def persist_events(df: pd.DataFrame, replace: bool = True) -> int:
    init_db()
    conn = get_connection()
    try:
        if replace:
            conn.execute("DELETE FROM network_events")
            conn.execute("DELETE FROM alerts")
            conn.execute("DELETE FROM incidents")
            conn.execute("DELETE FROM analysis_runs")
        df = df.copy()
        if "failed_attempts" not in df.columns:
            df["failed_attempts"] = 0
        if "is_suspicious" not in df.columns:
            df["is_suspicious"] = 0
        df.to_sql("network_events", conn, if_exists="append", index=False)
        conn.commit()
        return len(df)
    finally:
        conn.close()


def fetch_events() -> pd.DataFrame:
    conn = get_connection()
    try:
        return pd.read_sql_query("SELECT * FROM network_events", conn)
    finally:
        conn.close()