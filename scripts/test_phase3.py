"""
Phase 3 test — ML + Correlation + Risk.
Run: python scripts/test_phase3.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data_loader import load_csv
from src.preprocessing import preprocess
from src.detection import (
    detect_port_scans, detect_brute_force, detect_traffic_floods,
    detect_traffic_anomalies, detect_protocol_anomalies,
)
from src.anomaly.isolation_forest import detect_ml_anomalies
from src.correlation.incident_engine import correlate_alerts

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_network_logs.csv"


def main():
    print("[ThreatLens] Phase 3 Test — ML + Correlation + Risk\n")

    df = preprocess(load_csv(DATA_PATH))
    print(f"Loaded {len(df)} events\n")

    # ---------- Run all detectors ----------
    print("── Detection ──────────────────────────")
    all_alerts = []
    for name, fn in [
        ("Port Scan",        detect_port_scans),
        ("Brute Force",      detect_brute_force),
        ("Traffic Flood",    detect_traffic_floods),
        ("Traffic Anomaly",  detect_traffic_anomalies),
        ("Protocol Anomaly", detect_protocol_anomalies),
        ("ML Anomaly",       detect_ml_anomalies),
    ]:
        alerts = fn(df)
        print(f"  {name:<18} → {len(alerts)} alert(s)")
        all_alerts.extend([a.to_dict() for a in alerts])

    print(f"\nTotal alerts: {len(all_alerts)}")

    # ---------- Correlation ----------
    print("\n── Correlation ────────────────────────")
    incidents = correlate_alerts(all_alerts)
    print(f"Incidents created: {len(incidents)}\n")

    for inc in incidents:
        print("=" * 60)
        print(f"  {inc['title']}")
        print(f"  Source:      {inc['source_ip']}")
        print(f"  Window:      {inc['first_seen']} → {inc['last_seen']}")
        print(f"  Threats:     {len(inc['threat_types'])} types  "
              f"({', '.join(inc['threat_types'])})")
        print(f"  Alerts:      {inc['alert_count']}")
        print(f"  Base score:  {inc['base_score']}")
        print(f"  Bonus:       +{inc['correlation_bonus']}")
        print(f"  FINAL SCORE: {inc['risk_score']} / 100")
        print(f"  SEVERITY:    {inc['severity']}")
        print(f"  Description: {inc['description']}")
        print("=" * 60)


if __name__ == "__main__":
    main()