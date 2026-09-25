"""
ThreatLens — Isolation Forest anomaly detection.
Flags statistically unusual events that rule-based detectors may miss.
"""

import pandas as pd
from sklearn.ensemble import IsolationForest
from src.detection.base import Alert
from utils.constants import (
    THREAT_ML_ANOMALY, SCORE_ML_ANOMALY, SEV_MEDIUM,
)


FEATURE_COLS = [
    "packet_count",
    "packet_size",
    "bytes_transferred",
    "connection_duration",
    "failed_attempts",
]


def detect_ml_anomalies(df: pd.DataFrame, contamination: float = 0.02) -> list[Alert]:
    """
    Train Isolation Forest on numeric features and return alerts for outliers.
    Keeps only the TOP-N most anomalous events globally to avoid noise.
    """
    if df.empty or len(df) < 50:
        return []

    df = df.copy()

    # Ensure all feature columns exist
    for col in FEATURE_COLS:
        if col not in df.columns:
            df[col] = 0

    X = df[FEATURE_COLS].fillna(0).astype(float)

    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=42,
        n_jobs=-1,
    )
    preds = model.fit_predict(X)          # -1 = anomaly, 1 = normal
    scores = model.decision_function(X)   # lower = more anomalous

    anomalies = df[preds == -1].copy()
    anomalies["_ml_score"] = scores[preds == -1]

    alerts: list[Alert] = []

    # Global cap: keep only the TOP-N most anomalous events overall
    GLOBAL_ML_CAP = 8
    anomalies = anomalies.nsmallest(GLOBAL_ML_CAP, "_ml_score")

    for _, row in anomalies.iterrows():
        alerts.append(Alert(
            threat_type=THREAT_ML_ANOMALY,
            source_ip=row["source_ip"],
            destination_ip=row["destination_ip"],
            timestamp=row["timestamp"].isoformat(timespec="seconds"),
            severity=SEV_MEDIUM,
            risk_score=SCORE_ML_ANOMALY,
            description=f"Behavioural anomaly detected from {row['source_ip']}",
            evidence={
                "ml_score": round(float(row["_ml_score"]), 4),
                "packet_count": int(row["packet_count"]),
                "bytes_transferred": int(row["bytes_transferred"]),
                "failed_attempts": int(row["failed_attempts"]),
            },
        ))

    return alerts