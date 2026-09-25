"""
ThreatLens — Network Security Analytics & Intrusion Investigation Platform
Main entry point.
"""

import streamlit as st
from utils.ui import (
    inject_css, topbar, section_header, card_row,
    walkthrough_card, expandable_service_card, get_current_theme
)

st.set_page_config(
    page_title="ThreatLens · Network Security Analytics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
topbar(status_text="SYSTEM READY", status="good")

theme = get_current_theme()
badge_bg = "rgba(79, 70, 229, 0.08)" if theme == "light" else "rgba(0, 242, 254, 0.12)"
badge_border = "rgba(79, 70, 229, 0.22)" if theme == "light" else "rgba(0, 242, 254, 0.3)"
badge_color = "#4F46E5" if theme == "light" else "#00F2FE"
sub_color = "#64748B" if theme == "light" else "#94A3B8"

# ----------------------------------------------------
# 1. HERO SECTION
# ----------------------------------------------------
st.markdown(f"""
<div class="tl-hero">
  <div class="tl-hero-badge" style="background:{badge_bg};border:1px solid {badge_border};color:{badge_color};">
    <span>🛡️</span> NEXT-GEN SECURITY OPERATIONS PLATFORM
  </div>
  <h1 class="tl-hero-title">ThreatLens</h1>
  <div class="tl-hero-subtitle" style="color:{sub_color};">
    Transform high-volume raw network telemetry into structured, high-fidelity security incidents. Click any service card below to expand details or launch.
  </div>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. CORE ARCHITECTURE METRIC CARDS (Exact Screenshot Row)
# ----------------------------------------------------
st.markdown(f"""
<div style="font-size:12px;font-weight:600;color:{sub_color};margin:4px 0 8px 2px;">
  High-throughput detection and correlation engine
</div>
""", unsafe_allow_html=True)

card_row([
    {"label": "DETECTION ENGINE", "value": "5 Rules", "delta": "Deterministic"},
    {"label": "ML TELEMETRY", "value": "IsoForest", "delta": "Unsupervised"},
    {"label": "CORRELATION", "value": "Attacker IP", "delta": "Graph-aware"},
    {"label": "RISK SCORING", "value": "0–100", "delta": "Explainable"},
])

st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

# ----------------------------------------------------
# 3. PIPELINE WALKTHROUGH (Exact 3 Cards from Screenshot)
# ----------------------------------------------------
section_header("🚀", "Pipeline Walkthrough", "Three seamless steps from telemetry to mitigation")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        walkthrough_card(
            phase="PHASE 01",
            title="Ingest & Analyze",
            description="Feed 25,000+ network event flows through multi-stage anomaly detection filters."
        ),
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        walkthrough_card(
            phase="PHASE 02",
            title="Incident Correlation",
            description="Group disparate port scans, credential stuffing, and flood alerts into unified attacker entities."
        ),
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        walkthrough_card(
            phase="PHASE 03",
            title="Deep-Dive Forensics",
            description="Inspect forensic timelines, protocol breakdowns, and evidence traces for rapid response."
        ),
        unsafe_allow_html=True
    )

st.markdown("<hr/>", unsafe_allow_html=True)

# ----------------------------------------------------
# 4. COMPACT EXPANDABLE SERVICE CARDS (3 Columns x 2 Rows)
# ----------------------------------------------------
section_header("🎯", "Security Operations & Services", "Click any service card to expand capabilities or launch directly")

row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    st.markdown(
        expandable_service_card(
            badge="REAL-TIME OPS",
            title="📊 SOC Operations",
            short_desc="Live event throughput, network bandwidth graphs, and attack vectors.",
            full_desc="Live event throughput, network bandwidth graphs, attack vector distribution, and active incident alerts.",
            bullets=[
                "⚡ 25,000+ Ingested Flow Events",
                "🚨 5-Tier Threat Vector Breakdown",
                "📈 Dynamic Real-Time Traffic Timeline",
                "⚠️ Severity Ratios (Low → Critical)",
            ],
            link_url="/SOC_Operations",
            link_label="Launch Operations Center →"
        ),
        unsafe_allow_html=True
    )

with row1_col2:
    st.markdown(
        expandable_service_card(
            badge="DETECTION ML",
            title="🚀 Intrusion Scanner",
            short_desc="5 deterministic intrusion rules + unsupervised Isolation Forest.",
            full_desc="Run 5 deterministic intrusion rules plus unsupervised Isolation Forest to detect volumetric floods, stealth scans, and credential attacks.",
            bullets=[
                "🛡️ Port Scan & Brute Force Rules",
                "🤖 Isolation Forest Anomaly ML",
                "🌊 Volumetric SYN Flood Detection",
                "📤 Custom Network Log CSV Upload",
            ],
            link_url="/Intrusion_Scanner",
            link_label="Launch Intrusion Scanner →"
        ),
        unsafe_allow_html=True
    )

with row1_col3:
    st.markdown(
        expandable_service_card(
            badge="CORRELATION",
            title="🚨 Active Incidents",
            short_desc="Multi-vector alert clustering into unified attacker IP entities.",
            full_desc="Automated threat correlation linking multi-vector alerts to unique attacker IPs with explainable risk scoring.",
            bullets=[
                "🔗 Attacker IP Entity Clustering",
                "💯 Explainable 0–100 Risk Score",
                "💥 Multi-Signal Correlation Bonus (+10)",
                "📜 Chronological Attack Progression",
            ],
            link_url="/Active_Incidents",
            link_label="Investigate Incidents →"
        ),
        unsafe_allow_html=True
    )

row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.markdown(
        expandable_service_card(
            badge="PACKET FLOWS",
            title="📈 Network Telemetry",
            short_desc="Protocol compositions, firewall accept rates, and bandwidth.",
            full_desc="Transport protocol composition (TCP, UDP, ICMP), firewall acceptance ratios (ALLOW vs DENY), and bandwidth timelines.",
            bullets=[
                "🔀 Protocol Distribution (TCP/UDP/ICMP)",
                "📊 Connection Acceptance Rates",
                "💾 Bandwidth Over Time (MB/min)",
                "🌐 Top Source & Target Endpoint IPs",
            ],
            link_url="/Network_Telemetry",
            link_label="Explore Network Telemetry →"
        ),
        unsafe_allow_html=True
    )

with row2_col2:
    st.markdown(
        expandable_service_card(
            badge="DEEP FORENSICS",
            title="🔎 Entity Forensics",
            short_desc="Targeted host behavioral profiling, attack timelines, JSON traces.",
            full_desc="Deep-dive behavioral profiling, chronological attack timeline reconstruction, and raw JSON evidence inspection.",
            bullets=[
                "📜 Chronological Attack Timelines",
                "🔍 Structured JSON Payload Traces",
                "⚠️ Host Behavioral Risk Profiles",
                "🎯 MITRE ATT&CK Tactic Alignment",
            ],
            link_url="/Entity_Forensics",
            link_label="Open Forensics Workbench →"
        ),
        unsafe_allow_html=True
    )

with row2_col3:
    st.markdown(
        expandable_service_card(
            badge="EXPLAINABLE AI",
            title="🛡️ Scoring Model",
            short_desc="Deterministic base weights + correlation multiplier logic.",
            full_desc="Multi-signal risk allocation model combining deterministic rule weights with graph correlation bonuses.",
            bullets=[
                "🎯 Port Scan: +22 pts (Reconnaissance)",
                "🔑 Brute Force: +18 pts (Credentials)",
                "🌊 Traffic Flood: +18 pts (Volumetric)",
                "🤖 ML IsoForest: +15 pts (Anomaly Outlier)",
            ],
            link_url="/Intrusion_Scanner",
            link_label="Test Scoring Engine →"
        ),
        unsafe_allow_html=True
    )

st.markdown("<hr/>", unsafe_allow_html=True)

# ----------------------------------------------------
# 5. DETECTION WEIGHT & SCORING MODEL (Exact Section from Screenshot)
# ----------------------------------------------------
section_header("🛡️", "Detection Weight & Scoring Model", "Explainable signal contributions and correlation multiplier")

card_row([
    {"label": "PORT SCAN RECON", "value": "+22 pts", "delta": "Deterministic"},
    {"label": "BRUTE FORCE AUTH", "value": "+18 pts", "delta": "Deterministic"},
    {"label": "SYN FLOOD D-DOS", "value": "+18 pts", "delta": "Deterministic"},
    {"label": "ISOFOREST ML", "value": "+15 pts", "delta": "Unsupervised"},
    {"label": "MULTI-SIGNAL CORRELATION", "value": "+10 pts", "delta": "Correlation Bonus"},
])

st.markdown("<hr/>", unsafe_allow_html=True)
st.caption("🛡️ Defensive security analytics · Built for production SOC environments and threat hunters")