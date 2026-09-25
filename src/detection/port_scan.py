"""
Port Scan detector.
Trigger: same source_ip hits >= 10 unique destination ports within 60s.
"""

import pandas as pd
from src.detection.base import Alert
from utils.constants import (
    PORT_SCAN_WINDOW_SEC, PORT_SCAN_MIN_UNIQUE_PORTS, PORT_SCAN_MIN_EVENTS,
    THREAT_PORT_SCAN, SCORE_PORT_SCAN,
    SEV_HIGH, SEV_CRITICAL,
)


def detect_port_scans(df: pd.DataFrame) -> list[Alert]:
    """Detect port scans. Returns list of Alert objects."""
    if df.empty:
        return []

    alerts: list[Alert] = []
    df = df.sort_values("timestamp").copy()

    for src_ip, group in df.groupby("source_ip"):
        group = group.sort_values("timestamp").reset_index(drop=True)
        times = group["timestamp"].tolist()
        ports = group["destination_port"].tolist()
        dests = group["destination_ip"].tolist()

        n = len(group)
        i = 0
        while i < n:
            j = i
            while (j < n and
                   (times[j] - times[i]).total_seconds() <= PORT_SCAN_WINDOW_SEC):
                j += 1

            window = group.iloc[i:j]
            unique_ports = window["destination_port"].nunique()
            event_count = len(window)

            if (unique_ports >= PORT_SCAN_MIN_UNIQUE_PORTS and
                    event_count >= PORT_SCAN_MIN_EVENTS):
                window_seconds = (times[j - 1] - times[i]).total_seconds()
                severity = (SEV_CRITICAL if unique_ports > 20
                            else SEV_HIGH)

                alerts.append(Alert(
                    threat_type=THREAT_PORT_SCAN,
                    source_ip=src_ip,
                    destination_ip=dests[i],
                    timestamp=times[i].isoformat(timespec="seconds"),
                    severity=severity,
                    risk_score=SCORE_PORT_SCAN,
                    description=f"Potential port scan from {src_ip}",
                    evidence={
                        "unique_ports": int(unique_ports),
                        "events_in_window": int(event_count),
                        "window_seconds": float(window_seconds),
                        "sample_ports": sorted(window["destination_port"]
                                               .unique().tolist())[:10],
                    },
                ))
                # Skip past this window to avoid duplicate alerts
                i = j
            else:
                i += 1

    return alerts