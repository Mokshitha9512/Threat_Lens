"""ThreatLens — IP Investigation."""

import streamlit as st
import pandas as pd
from utils.state import get_data
from utils.ui import (
    inject_css, topbar, section_header, severity_badge,
    get_current_theme
)

st.set_page_config(page_title="Entity Forensics · ThreatLens",
                   page_icon="🔎", layout="wide")

inject_css()
df, alerts, incidents = get_data()

theme = get_current_theme()
sub_color = "#64748B" if theme == "light" else "#94A3B8"
title_color = "#0F172A" if theme == "light" else "#F8FAFC"
accent_color = "#4F46E5" if theme == "light" else "#00F2FE"
accent_glow = "rgba(79, 70, 229, 0.4)" if theme == "light" else "rgba(0, 242, 254, 0.6)"

topbar(status_text="INVESTIGATION WORKBENCH ACTIVE", status="warn")

section_header("🔎", "Host & Attacker IP Forensics",
               "Targeted deep-dive into entity behavioral profiles, threat vectors, and evidence payloads")

all_ips = sorted(df["source_ip"].unique().tolist())
default_ip = "192.168.1.50" if "192.168.1.50" in all_ips else all_ips[0]
selected_ip = st.selectbox("Select Target Source IP for Forensic Inspection", all_ips,
                            index=all_ips.index(default_ip))

ip_df        = df[df["source_ip"] == selected_ip]
ip_alerts    = [a for a in alerts if a["source_ip"] == selected_ip]
ip_incidents = [i for i in incidents if i["source_ip"] == selected_ip]

risk_score = ip_incidents[0]["risk_score"] if ip_incidents else 0
severity   = ip_incidents[0]["severity"] if ip_incidents else "LOW"
sev_badge  = severity_badge(severity)

# ---------- Summary Cards ----------
section_header("📊", "Entity Profile Summary", f"Telemetry activity overview for {selected_ip}")

crit_class = "crit" if risk_score > 70 else ("warn" if risk_score > 25 else "good")

st.markdown(f"""
<div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:20px;">
  <div class="tl-card" style="flex:1;min-width:160px;">
    <div class="tl-card-label">Total Flow Records</div>
    <div class="tl-card-value">{len(ip_df):,}</div>
  </div>
  <div class="tl-card {'warn' if ip_alerts else ''}" style="flex:1;min-width:160px;">
    <div class="tl-card-label">Triggered Alerts</div>
    <div class="tl-card-value">{len(ip_alerts)}</div>
  </div>
  <div class="tl-card {'crit' if ip_incidents else 'good'}" style="flex:1;min-width:160px;">
    <div class="tl-card-label">Correlated Incidents</div>
    <div class="tl-card-value">{len(ip_incidents)}</div>
  </div>
  <div class="tl-card {crit_class}" style="flex:1;min-width:160px;">
    <div class="tl-card-label">Threat Severity</div>
    <div style="margin-top:6px;">{sev_badge}</div>
  </div>
  <div class="tl-card {crit_class}" style="flex:1;min-width:160px;">
    <div class="tl-card-label">Risk Index</div>
    <div class="tl-card-value">{risk_score}<span style="font-size:14px;color:{sub_color};font-weight:600;">/100</span></div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- Threat Breakdown ----------
if ip_alerts:
    section_header("⚠️", "Identified Threat Vector Distribution")
    breakdown = pd.DataFrame(ip_alerts)["threat_type"].value_counts().reset_index()
    breakdown.columns = ["Attack Vector", "Incident Occurrences"]
    st.dataframe(breakdown, use_container_width=True, hide_index=True)

# ---------- Behaviour Timeline ----------
section_header("📜", "Chronological Behavior Timeline")
if ip_alerts:
    timeline_alerts = sorted(ip_alerts, key=lambda x: x["timestamp"])
    html = f'<div style="border-left:3px solid {accent_color};padding-left:22px;margin:16px 0 20px 8px;">'
    for a in timeline_alerts:
        a_badge = severity_badge(a.get("severity", "MEDIUM"))
        html += (
            f'<div style="margin-bottom:18px;position:relative;">'
            f'<div style="position:absolute;left:-29px;top:4px;width:12px;height:12px;'
            f'border-radius:50%;background:{accent_color};box-shadow:0 0 10px {accent_glow};"></div>'
            f'<div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">'
            f'<span style="font-family:\'JetBrains Mono\',monospace;color:{sub_color};font-size:12px;font-weight:600;">{a["timestamp"]}</span>'
            f'{a_badge}'
            f'</div>'
            f'<div style="color:{title_color};font-size:15px;font-weight:700;margin-top:4px;">'
            f'{a["threat_type"]}'
            f'</div>'
            f'<div style="color:{sub_color};font-size:13px;margin-top:2px;">{a.get("description", "")}</div>'
            f'</div>'
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
else:
    st.info("No suspicious or anomalous activities recorded for this IP address.")

# ---------- Why Suspicious ----------
if ip_alerts:
    section_header("🧠", "Forensic Signal & Telemetry Evidence")
    for a in ip_alerts[:6]:
        with st.expander(f"{a['threat_type']} — {a['timestamp']} [{a['severity']}]"):
            st.markdown(f"**Vector Synthesis:** {a.get('description', '')}")
            st.markdown("**Evidence Payload:**")
            st.json(a.get("evidence_json", {}))

# ---------- Raw Events ----------
section_header("🗂️", "Sample Raw Event Stream (Last 30 Flows)")
st.dataframe(ip_df.head(30), use_container_width=True, hide_index=True)