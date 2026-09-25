"""
Traffic Flood detector.
Trigger: events/min from a source exceeds baseline * 4.
"""

import pandas as pd
from src.detection.base import Alert
from utils.constants import (
    TRAFFIC_FLOOD_MULTIPLIER,
    THREAT_TRAFFIC_FLOOD, SCORE_TRAFFIC_FLOOD,
    SEV_HIGH, SEV_CRITICAL,
)


def detect_traffic_floods(df: pd.DataFrame) -> list[Alert]:
    if df.empty:
        return []

    alerts: list[Alert] = []
    df = df.copy()
    df["minute"] = df["timestamp"].dt.floor("min")

    per_minute = (df.groupby(["source_ip", "minute"])
                    .size()
                    .reset_index(name="events_per_min"))

    # GLOBAL baseline — used when a source IP has too little history
    global_baseline = per_minute["events_per_min"].median()
    if global_baseline <= 0:
        global_baseline = 1

    for src_ip, group in per_minute.groupby("source_ip"):
        local_baseline = group["events_per_min"].median()

        # Use local baseline only if enough data AND non-trivial
        baseline = (local_baseline
                    if len(group) >= 5 and local_baseline > 0
                    else global_baseline)

        threshold = baseline * TRAFFIC_FLOOD_MULTIPLIER

        for _, row in group.iterrows():
            if row["events_per_min"] > threshold:
                multiplier = row["events_per_min"] / baseline
                sev = SEV_CRITICAL if multiplier > 8 else SEV_HIGH

                alerts.append(Alert(
                    threat_type=THREAT_TRAFFIC_FLOOD,
                    source_ip=src_ip,
                    destination_ip="*",
                    timestamp=row["minute"].isoformat(timespec="seconds"),
                    severity=sev,
                    risk_score=SCORE_TRAFFIC_FLOOD,
                    description=f"Traffic spike from {src_ip}",
                    evidence={
                        "events_per_min": int(row["events_per_min"]),
                        "baseline": round(float(baseline), 2),
                        "multiplier": round(float(multiplier), 2),
                    },
                ))

    return alerts