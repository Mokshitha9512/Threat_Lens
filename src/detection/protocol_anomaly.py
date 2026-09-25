"""
Protocol Anomaly detector.
Trigger: unusual protocol ↔ port pairing (e.g. UDP on port 22).
"""

import pandas as pd
from src.detection.base import Alert
from utils.constants import (
    THREAT_PROTOCOL_ANOMALY, SCORE_PROTOCOL_ANOMALY, SEV_MEDIUM,
)

# Expected protocol for well-known ports
EXPECTED_PROTOCOL = {
    22:   {"TCP"},
    23:   {"TCP"},
    25:   {"TCP"},
    53:   {"UDP", "TCP"},
    80:   {"TCP"},
    110:  {"TCP"},
    143:  {"TCP"},
    443:  {"TCP"},
    445:  {"TCP"},
    3306: {"TCP"},
    3389: {"TCP"},
}


def detect_protocol_anomalies(df: pd.DataFrame) -> list[Alert]:
    """Only flag protocol↔port mismatches that are rare overall (<1% of traffic)."""
    if df.empty:
        return []

    alerts: list[Alert] = []
    df = df.copy()
    df["protocol"] = df["protocol"].str.upper()

    total = len(df)
    pair_counts = df.groupby(["destination_port", "protocol"]).size().to_dict()

    candidates = df[df["destination_port"].isin(EXPECTED_PROTOCOL)]
    for _, row in candidates.iterrows():
        port = row["destination_port"]
        proto = row["protocol"]

        if proto in EXPECTED_PROTOCOL[port]:
            continue

        # Rare-event filter: this (port, proto) pair must be < 0.5% of ALL traffic
        pair_count = pair_counts.get((port, proto), 0)
        if pair_count / total > 0.005:
            continue

        alerts.append(Alert(
            threat_type=THREAT_PROTOCOL_ANOMALY,
            source_ip=row["source_ip"],
            destination_ip=row["destination_ip"],
            timestamp=row["timestamp"].isoformat(timespec="seconds"),
            severity=SEV_MEDIUM,
            risk_score=SCORE_PROTOCOL_ANOMALY,
            description=f"Unusual {proto} traffic on port {port}",
            evidence={
                "protocol": proto,
                "destination_port": int(port),
                "expected": sorted(EXPECTED_PROTOCOL[port]),
                "occurrences": int(pair_count),
            },
        ))

    return alerts