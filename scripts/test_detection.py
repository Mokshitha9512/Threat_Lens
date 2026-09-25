"""
Quick end-to-end test of Phase 2 detection.
Run: python scripts/test_detection.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
from src.data_loader import load_csv
from src.preprocessing import preprocess
from src.detection import (
    detect_port_scans, detect_brute_force, detect_traffic_floods,
    detect_traffic_anomalies, detect_protocol_anomalies,
)

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_network_logs.csv"


def main():
    print("[ThreatLens] Loading dataset...")
    df = load_csv(DATA_PATH)
    df = preprocess(df)
    print(f"[ThreatLens] Loaded {len(df)} events\n")

    print("=" * 60)
    print("RUNNING DETECTION ENGINE")
    print("=" * 60)

    results = {
        "Port Scan":        detect_port_scans(df),
        "Brute Force":      detect_brute_force(df),
        "Traffic Flood":    detect_traffic_floods(df),
        "Traffic Anomaly":  detect_traffic_anomalies(df),
        "Protocol Anomaly": detect_protocol_anomalies(df),
    }

    total = 0
    for name, alerts in results.items():
        print(f"\n[{name}] → {len(alerts)} alert(s)")
        for a in alerts[:3]:    # show first 3 of each
            print(f"   ├─ {a.timestamp}  {a.source_ip}  "
                  f"[{a.severity}]  score={a.risk_score}")
            print(f"   │  {a.description}")
            print(f"   │  evidence: {a.evidence}")
        if len(alerts) > 3:
            print(f"   └─ ... and {len(alerts) - 3} more")
        total += len(alerts)

    print("\n" + "=" * 60)
    print(f"TOTAL ALERTS GENERATED: {total}")
    print("=" * 60)


if __name__ == "__main__":
    main()