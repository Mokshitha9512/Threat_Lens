"""ThreatLens — clean and normalise raw event data."""

import pandas as pd


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp", "source_ip", "destination_ip"])

    for col in ["source_port", "destination_port", "packet_count",
                "packet_size", "bytes_transferred", "failed_attempts"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    df["connection_duration"] = pd.to_numeric(
        df.get("connection_duration", 0), errors="coerce"
    ).fillna(0.0)

    df["protocol"] = df["protocol"].astype(str).str.upper().str.strip()
    df["status"]   = df["status"].astype(str).str.upper().str.strip()
    df["source_ip"]      = df["source_ip"].astype(str).str.strip()
    df["destination_ip"] = df["destination_ip"].astype(str).str.strip()

    df = df.sort_values("timestamp").reset_index(drop=True)
    return df