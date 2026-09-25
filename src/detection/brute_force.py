"""
Brute Force detector.
Trigger: >= 10 FAILED auth events from same src→dst within 5 min.
"""

import pandas as pd
from src.detection.base import Alert
from utils.constants import (
    BRUTE_FORCE_WINDOW_SEC, BRUTE_FORCE_MIN_FAILURES,
    THREAT_BRUTE_FORCE, SCORE_BRUTE_FORCE,
    SEV_MEDIUM, SEV_HIGH, SEV_CRITICAL,
    STATUS_FAILED, STATUS_DENIED,
)


def detect_brute_force(df: pd.DataFrame) -> list[Alert]:
    if df.empty:
        return []

    alerts: list[Alert] = []
    failed = df[df["status"].isin([STATUS_FAILED, STATUS_DENIED])].copy()
    if failed.empty:
        return []

    failed = failed.sort_values("timestamp")

    for (src, dst), group in failed.groupby(["source_ip", "destination_ip"]):
        group = group.sort_values("timestamp").reset_index(drop=True)
        times = group["timestamp"].tolist()
        n = len(group)

        i = 0
        while i < n:
            j = i
            while (j < n and
                   (times[j] - times[i]).total_seconds() <= BRUTE_FORCE_WINDOW_SEC):
                j += 1

            count = j - i
            if count >= BRUTE_FORCE_MIN_FAILURES:
                if count >= 25:
                    sev = SEV_CRITICAL
                elif count >= 15:
                    sev = SEV_HIGH
                else:
                    sev = SEV_MEDIUM

                target_port = int(group.iloc[i]["destination_port"])
                alerts.append(Alert(
                    threat_type=THREAT_BRUTE_FORCE,
                    source_ip=src,
                    destination_ip=dst,
                    timestamp=times[i].isoformat(timespec="seconds"),
                    severity=sev,
                    risk_score=SCORE_BRUTE_FORCE,
                    description=f"Repeated failed authentications against {dst}",
                    evidence={
                        "failed_count": int(count),
                        "target_port": target_port,
                        "window_seconds": BRUTE_FORCE_WINDOW_SEC,
                    },
                ))
                i = j
            else:
                i += 1

    return alerts