"""ThreatLens — shared session state + cached pipeline runner."""

import streamlit as st
import pandas as pd
from pathlib import Path

from src.data_loader import load_csv
from src.preprocessing import preprocess
from src.detection import (
    detect_port_scans, detect_brute_force, detect_traffic_floods,
    detect_traffic_anomalies, detect_protocol_anomalies,
)
from src.anomaly.isolation_forest import detect_ml_anomalies
from src.correlation.incident_engine import correlate_alerts

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_network_logs.csv"


def ensure_analyzed():
    if st.session_state.get("analyzed"):
        return

    try:
        df = preprocess(load_csv(DATA_PATH))

        alerts = []
        for fn in [
            detect_port_scans, detect_brute_force, detect_traffic_floods,
            detect_traffic_anomalies, detect_protocol_anomalies,
            detect_ml_anomalies,
        ]:
            alerts.extend([a.to_dict() for a in fn(df)])

        incidents = correlate_alerts(alerts)

        st.session_state["df"]        = df
        st.session_state["alerts"]    = alerts
        st.session_state["incidents"] = incidents
        st.session_state["analyzed"]  = True
    except Exception as e:
        # Show the real error instead of silent blank page
        st.error(f"Pipeline error: {type(e).__name__}: {e}")
        import traceback
        st.code(traceback.format_exc())
        st.stop()


def get_data():
    ensure_analyzed()
    return (
        st.session_state.get("df", pd.DataFrame()),
        st.session_state.get("alerts", []),
        st.session_state.get("incidents", []),
    )