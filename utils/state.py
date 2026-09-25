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


@st.cache_data(show_spinner=False)
def load_and_analyze_default():
    """Runs pipeline once and caches data/alerts/incidents across all pages and sessions."""
    df = preprocess(load_csv(DATA_PATH))

    alerts = []
    for fn in [
        detect_port_scans, detect_brute_force, detect_traffic_floods,
        detect_traffic_anomalies, detect_protocol_anomalies,
        detect_ml_anomalies,
    ]:
        alerts.extend([a.to_dict() for a in fn(df)])

    incidents = correlate_alerts(alerts)
    return df, alerts, incidents


def set_custom_data(df: pd.DataFrame, alerts: list, incidents: list, source_name: str = "Custom Upload"):
    """Stores custom analyzed telemetry into session state for all pages to use."""
    st.session_state["custom_df"] = df
    st.session_state["custom_alerts"] = alerts
    st.session_state["custom_incidents"] = incidents
    st.session_state["source_name"] = source_name
    st.session_state["df"] = df
    st.session_state["alerts"] = alerts
    st.session_state["incidents"] = incidents
    st.session_state["analyzed"] = True


def reset_to_default():
    """Clears custom data and restores the default enterprise telemetry."""
    st.session_state.pop("custom_df", None)
    st.session_state.pop("custom_alerts", None)
    st.session_state.pop("custom_incidents", None)
    st.session_state.pop("source_name", None)
    df, alerts, incidents = load_and_analyze_default()
    st.session_state["df"] = df
    st.session_state["alerts"] = alerts
    st.session_state["incidents"] = incidents
    st.session_state["analyzed"] = True
    return df, alerts, incidents


def get_data():
    """Returns (df, alerts, incidents). Uses custom uploaded data if present, otherwise instant cached default."""
    if "custom_df" in st.session_state:
        return (
            st.session_state.get("custom_df", pd.DataFrame()),
            st.session_state.get("custom_alerts", []),
            st.session_state.get("custom_incidents", []),
        )

    df, alerts, incidents = load_and_analyze_default()
    st.session_state["df"] = df
    st.session_state["alerts"] = alerts
    st.session_state["incidents"] = incidents
    st.session_state["analyzed"] = True
    return df, alerts, incidents