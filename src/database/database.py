"""ThreatLens — SQLite database layer."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "threatlens.db"


SCHEMA = """
CREATE TABLE IF NOT EXISTS network_events (
    event_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp           TEXT    NOT NULL,
    source_ip           TEXT    NOT NULL,
    destination_ip      TEXT    NOT NULL,
    source_port         INTEGER,
    destination_port    INTEGER,
    protocol            TEXT,
    packet_count        INTEGER,
    packet_size         INTEGER,
    bytes_transferred   INTEGER,
    connection_duration REAL,
    status              TEXT,
    failed_attempts     INTEGER DEFAULT 0,
    is_suspicious       INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS alerts (
    alert_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp       TEXT    NOT NULL,
    source_ip       TEXT    NOT NULL,
    destination_ip  TEXT,
    threat_type     TEXT    NOT NULL,
    severity        TEXT    NOT NULL,
    risk_score      INTEGER NOT NULL,
    description     TEXT,
    evidence_json   TEXT,
    incident_id     INTEGER,
    status          TEXT DEFAULT 'OPEN'
);

CREATE TABLE IF NOT EXISTS incidents (
    incident_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at      TEXT,
    first_seen      TEXT,
    last_seen       TEXT,
    source_ip       TEXT,
    severity        TEXT,
    risk_score      INTEGER,
    title           TEXT,
    description     TEXT,
    status          TEXT DEFAULT 'OPEN'
);

CREATE TABLE IF NOT EXISTS analysis_runs (
    run_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    filename          TEXT,
    timestamp         TEXT,
    total_events      INTEGER,
    total_threats     INTEGER,
    critical_threats  INTEGER,
    average_risk      REAL
);

CREATE INDEX IF NOT EXISTS idx_events_ts        ON network_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_src       ON network_events(source_ip);
CREATE INDEX IF NOT EXISTS idx_alerts_src       ON alerts(source_ip);
CREATE INDEX IF NOT EXISTS idx_alerts_incident  ON alerts(incident_id);
"""


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()


def reset_db() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
    init_db()


if __name__ == "__main__":
    init_db()
    print(f"[ThreatLens] Database ready at {DB_PATH}")