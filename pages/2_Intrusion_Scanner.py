"""ThreatLens — Analyze Network Data."""

import streamlit as st
import pandas as pd
from pathlib import Path
from utils.state import get_data, DATA_PATH
from utils.ui import (
    inject_css, topbar, section_header, card_row,
    get_current_theme, severity_badge
)
from src.preprocessing import preprocess
from src.detection import (
    detect_port_scans, detect_brute_force, detect_traffic_floods,
    detect_traffic_anomalies, detect_protocol_anomalies,
)
from src.anomaly.isolation_forest import detect_ml_anomalies
from src.correlation.incident_engine import correlate_alerts

st.set_page_config(page_title="Intrusion Scanner · ThreatLens", page_icon="🚀", layout="wide")

inject_css()
df, alerts, incidents = get_data()

theme = get_current_theme()
sub_color = "#64748B" if theme == "light" else "#94A3B8"
title_color = "#0F172A" if theme == "light" else "#F8FAFC"
accent_color = "#4F46E5" if theme == "light" else "#00F2FE"
badge_bg = "rgba(79, 70, 229, 0.1)" if theme == "light" else "rgba(0, 242, 254, 0.15)"
badge_border = "rgba(79, 70, 229, 0.25)" if theme == "light" else "rgba(0, 242, 254, 0.35)"

if incidents:
    topbar(status_text=f"⚠ INTRUSION ENGINE ACTIVE · {len(incidents)} CORRELATED THREAT ENTITY", status="crit")
else:
    topbar(status_text="DETECTION ENGINE ACTIVE · READY", status="good")

section_header("🚀", "Intrusion Detection & Correlation Engine",
               "Multi-stage intrusion pipeline executing 5 deterministic rules and unsupervised Isolation Forest ML")

tab1, tab2 = st.tabs(["🎬 Coordinated Attack Analysis", "📤 Upload Custom Telemetry"])

with tab1:
    st.markdown(f"""
    <div class="tl-card" style="margin: 14px 0 20px 0;">
      <div class="tl-card-label">Simulated Enterprise Intrusion Scenario · Attack Vector Progression</div>
      <div style="margin-top: 14px; display: flex; flex-direction: column; gap: 12px;">
        <div style="display: flex; align-items: center; gap: 14px;">
          <span style="font-family:'JetBrains Mono',monospace;font-weight:700;padding:3px 10px;border-radius:6px;background:{badge_bg};border:1px solid {badge_border};color:{accent_color};font-size:12px;">10:31</span>
          <span style="font-weight:700;color:{title_color};font-size:14px;min-width:140px;">Port Scan</span>
          <span style="color:{sub_color};font-size:13px;">Horizontal host discovery and reconnaissance targeting open service ports</span>
        </div>
        <div style="display: flex; align-items: center; gap: 14px;">
          <span style="font-family:'JetBrains Mono',monospace;font-weight:700;padding:3px 10px;border-radius:6px;background:{badge_bg};border:1px solid {badge_border};color:{accent_color};font-size:12px;">10:33</span>
          <span style="font-weight:700;color:{title_color};font-size:14px;min-width:140px;">Brute Force</span>
          <span style="color:{sub_color};font-size:13px;">High-frequency credential spraying attack on authentication endpoints</span>
        </div>
        <div style="display: flex; align-items: center; gap: 14px;">
          <span style="font-family:'JetBrains Mono',monospace;font-weight:700;padding:3px 10px;border-radius:6px;background:{badge_bg};border:1px solid {badge_border};color:{accent_color};font-size:12px;">10:34</span>
          <span style="font-weight:700;color:{title_color};font-size:14px;min-width:140px;">Traffic Flood</span>
          <span style="color:{sub_color};font-size:13px;">Volumetric SYN flood burst intended to saturate defensives and obscure exfiltration</span>
        </div>
        <div style="display: flex; align-items: center; gap: 14px;">
          <span style="font-family:'JetBrains Mono',monospace;font-weight:700;padding:3px 10px;border-radius:6px;background:{badge_bg};border:1px solid {badge_border};color:{accent_color};font-size:12px;">10:35</span>
          <span style="font-weight:700;color:{title_color};font-size:14px;min-width:140px;">Protocol Anomaly</span>
          <span style="color:{sub_color};font-size:13px;">Evasive non-standard payloads and anomalous packet length distribution</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c_btn, c_stat = st.columns([1, 2])
    with c_btn:
        re_run = st.button("🔄 Re-Run Detection & Correlation Pipeline", type="primary", use_container_width=True)

    if re_run:
        with st.spinner("Processing network packets & evaluating ML Isolation Forest..."):
            st.session_state.pop("analyzed", None)
            df, alerts, incidents = get_data()
        st.success(f"✅ Detection pipeline executed — {len(df):,} network flows evaluated.")

    # Live evaluation results (always visible)
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    section_header("📊", "Current Engine Results", "Real-time evaluation status across all detector modules")

    card_row([
        {"label": "Total Events Evaluated", "value": f"{len(df):,}", "delta": "Processed"},
        {"label": "Alerts Generated", "value": f"{len(alerts):,}", "variant": "warn"},
        {"label": "Correlated Threat Entities", "value": str(len(incidents)), "variant": "crit" if incidents else "good"},
    ])

    if incidents:
        inc = incidents[0]
        badge = severity_badge(inc["severity"])
        st.markdown(f"""
        <div class="tl-card crit" style="margin-top:20px;">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <div class="tl-card-label">🚨 Top Correlated Incident Dossier</div>
            <div>{badge}</div>
          </div>
          <div style="font-size:20px;font-weight:800;margin-top:6px;">
            {inc['title']}
          </div>
          <div style="color:{sub_color};font-size:14px;margin-top:10px;line-height:1.9;">
            <b>Attacker Source IP:</b> <code>{inc['source_ip']}</code><br/>
            <b>Capture Window:</b> {inc['first_seen']} → {inc['last_seen']}<br/>
            <b>Overall Risk Score:</b> <b style="color:#DC2626;">{inc['risk_score']}/100</b> ({inc['severity']})<br/>
            <b>Contributing Attack Vectors:</b> {', '.join(inc['threat_types'])}
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.page_link("pages/3_Active_Incidents.py", label="Open Active Incident Investigation →", icon="🚨")

with tab2:
    st.markdown("### Upload Custom Network Log CSV")
    st.caption("Required columns: timestamp, source_ip, destination_ip, destination_port, protocol, bytes_transferred, status")

    uploaded = st.file_uploader("Upload network flow CSV", type=["csv"], help="Select a CSV formatted network capture log")
    if uploaded is not None:
        try:
            df_up = pd.read_csv(uploaded)
            st.success(f"Successfully parsed {len(df_up):,} flow records from uploaded CSV.")
            st.dataframe(df_up.head(15), use_container_width=True)

            if st.button("🔍 Ingest & Analyze Uploaded Data", type="primary"):
                with st.spinner("Processing custom telemetry and running detection models..."):
                    df_proc = preprocess(df_up)
                    new_alerts = []
                    for fn in [
                        detect_port_scans, detect_brute_force, detect_traffic_floods,
                        detect_traffic_anomalies, detect_protocol_anomalies,
                        detect_ml_anomalies,
                    ]:
                        new_alerts.extend([a.to_dict() for a in fn(df_proc)])

                    new_incidents = correlate_alerts(new_alerts)
                    st.session_state["df"] = df_proc
                    st.session_state["alerts"] = new_alerts
                    st.session_state["incidents"] = new_incidents
                    st.session_state["analyzed"] = True

                st.success(f"✅ Ingestion complete! Found {len(new_alerts):,} alerts and {len(new_incidents)} correlated incidents. All sidebar views updated.")
                st.rerun()
        except Exception as e:
            st.error(f"Failed to process CSV: {e}")

    st.markdown("<hr/>", unsafe_allow_html=True)
    section_header("📁", "Enterprise Reference Dataset")
    if DATA_PATH.exists():
        df_sample = pd.read_csv(DATA_PATH)
        st.markdown(f"""
        <div class="tl-card">
          <div class="tl-card-label">Baseline Dataset Location</div>
          <div style="font-family:'JetBrains Mono',monospace;color:{accent_color};font-size:13px;margin:4px 0 14px 0;">
            {DATA_PATH}
          </div>
          <div style="display:flex;gap:30px;flex-wrap:wrap;">
            <div>
              <div class="tl-card-label">Total Flow Records</div>
              <div style="color:{title_color};font-size:20px;font-weight:800;">
                {len(df_sample):,}
              </div>
            </div>
            <div>
              <div class="tl-card-label">Schema Columns</div>
              <div style="color:{sub_color};font-size:13px;margin-top:4px;">
                {', '.join(df_sample.columns)}
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)