"""
Traffic Volume Anomaly detector.
Trigger: a single event's bytes_transferred is a strong outlier vs global baseline.
"""

import pandas as pd
from src.detection.base import Alert
from utils.constants import (
    TRAFFIC_ANOMALY_MULTIPLIER,
    THREAT_TRAFFIC_ANOMALY, SCORE_TRAFFIC_ANOMALY,
    SEV_MEDIUM, SEV_HIGH,
)


def detect_traffic_anomalies(df: pd.DataFrame) -> list[Alert]:
    if df.empty:
        return []

    alerts: list[Alert] = []
    df = df.copy()

    # Global baseline across ALL traffic
    global_median = df["bytes_transferred"].median()
    if global_median <= 0:
        return []

    threshold = global_median * TRAFFIC_ANOMALY_MULTIPLIER

    # Flag events whose bytes exceed threshold — but only keep unique ones
    # per source_ip so we don't fire hundreds of identical alerts
    spikes = df[df["bytes_transferred"] > threshold].copy()
    if spikes.empty:
        return []

    # One alert per source_ip (the largest spike)
    for src_ip, group in spikes.groupby("source_ip"):
        top = group.loc[group["bytes_transferred"].idxmax()]
        ratio = top["bytes_transferred"] / global_median
        sev = SEV_HIGH if ratio > 10 else SEV_MEDIUM

        alerts.append(Alert(
            threat_type=THREAT_TRAFFIC_ANOMALY,
            source_ip=src_ip,
            destination_ip=top["destination_ip"],
            timestamp=top["timestamp"].isoformat(timespec="seconds"),
            severity=sev,
            risk_score=SCORE_TRAFFIC_ANOMALY,
            description=f"Unusual data volume from {src_ip}",
            evidence={
                "peak_bytes": int(top["bytes_transferred"]),
                "baseline_bytes": round(float(global_median), 2),
                "ratio": round(float(ratio), 2),
                "spike_events": int(len(group)),
            },
        ))

    return alerts