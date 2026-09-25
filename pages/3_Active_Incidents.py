"""ThreatLens — Incidents Investigation."""

import streamlit as st
from utils.state import get_data
from utils.ui import (
    inject_css, topbar, section_header, severity_badge,
    get_current_theme
)

st.set_page_config(page_title="Active Incidents · ThreatLens", page_icon="🚨", layout="wide")

inject_css()
df, alerts, incidents = get_data()

theme = get_current_theme()
sub_color = "#64748B" if theme == "light" else "#94A3B8"
title_color = "#0F172A" if theme == "light" else "#F8FAFC"
accent_color = "#4F46E5" if theme == "light" else "#00F2FE"
accent_glow = "rgba(79, 70, 229, 0.4)" if theme == "light" else "rgba(0, 242, 254, 0.6)"
border_color = "#E2E8F0" if theme == "light" else "rgba(0, 242, 254, 0.2)"
bonus_color = "#059669" if theme == "light" else "#10E7A0"
crit_color = "#DC2626" if theme == "light" else "#FF6688"

if incidents:
    topbar(status_text=f"⚠ {len(incidents)} HIGH-PRIORITY INCIDENT(S) UNDER TRIAGE", status="crit")
else:
    topbar(status_text="NO ACTIVE INCIDENTS · ENVIRONMENT CLEAR", status="good")

section_header("🚨", "Incidents & Correlated Threats",
               "Coordinated multi-vector attacks grouped into consolidated incident dossiers")

if not incidents:
    st.markdown(f"""
    <div class="tl-card good" style="margin: 16px 0;">
      <div class="tl-card-label">✅ Threat Defense Status · Clear</div>
      <div style="font-size: 16px; font-weight: 700; color: {title_color}; margin-top: 6px;">
        No Active Correlated Incidents
      </div>
      <div style="color: {sub_color}; font-size: 13px; margin-top: 6px; line-height: 1.5;">
        All inspected packet flows and host endpoints conform to baseline security policies without multi-signal correlation flags.
      </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("⚡ Load Enterprise Intrusion Simulation Dataset", type="primary"):
        st.session_state.pop("analyzed", None)
        get_data()
        st.rerun()
    st.stop()

for idx, inc in enumerate(incidents):
    badge = severity_badge(inc["severity"])
    header = (f"🔥 {inc['title']}  —  Attacker: {inc['source_ip']}  "
              f"[{inc['risk_score']}/100 · {inc['severity']}]")

    with st.expander(header, expanded=(idx == 0)):
        # Summary row cards
        st.markdown(f"""
        <div style="display:flex;gap:14px;flex-wrap:wrap;margin:10px 0 20px 0;">
          <div class="tl-card crit" style="flex:1;min-width:160px;">
            <div class="tl-card-label">Aggregated Risk Score</div>
            <div class="tl-card-value">{inc['risk_score']}<span style="font-size:14px;color:{sub_color};font-weight:600;">/100</span></div>
          </div>
          <div class="tl-card" style="flex:1;min-width:160px;">
            <div class="tl-card-label">Classification</div>
            <div style="margin-top:6px;">{badge}</div>
          </div>
          <div class="tl-card" style="flex:1;min-width:160px;">
            <div class="tl-card-label">Total Alert Signals</div>
            <div class="tl-card-value">{inc['alert_count']}</div>
          </div>
          <div class="tl-card" style="flex:1;min-width:160px;">
            <div class="tl-card-label">Unique Attack Vectors</div>
            <div class="tl-card-value">{len(inc['threat_types'])}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"**Observed Time Window:** `{inc['first_seen']}` → `{inc['last_seen']}`")
        st.markdown(f"**Attacker IP Identity:** `{inc['source_ip']}`")
        st.markdown(f"**Automated Synthesis:** {inc['description']}")

        st.markdown("<hr/>", unsafe_allow_html=True)
        section_header("🧠", "Explainable Risk Allocation", "Deterministic scoring breakdown and multi-vector correlation multipliers")

        st.markdown(f"""
        <div class="tl-card" style="margin-bottom:14px;">
          <table style="width:100%;border-collapse:collapse;color:{title_color};">
            <tr style="border-bottom:1px solid {border_color};">
              <td style="padding:10px 0;font-size:14px;">Cumulative Base Score (Sum of individual vector alerts)</td>
              <td style="text-align:right;font-weight:700;font-size:15px;">{inc['base_score']}</td>
            </tr>
            <tr style="border-bottom:1px solid {border_color};">
              <td style="padding:10px 0;font-size:14px;">Multi-vector Correlation Bonus (3+ disparate threat vectors)</td>
              <td style="text-align:right;font-weight:800;color:{bonus_color};font-size:15px;">+{inc['correlation_bonus']}</td>
            </tr>
            <tr>
              <td style="padding:12px 0;font-weight:800;font-size:15px;">Calculated Final Threat Index</td>
              <td style="text-align:right;font-weight:800;color:{crit_color};font-size:20px;">
                {inc['risk_score']}<span style="font-size:13px;font-weight:600;color:{sub_color};">/100</span>
              </td>
            </tr>
          </table>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr/>", unsafe_allow_html=True)
        section_header("📜", "Chronological Attack Progression Timeline")

        timeline_alerts = sorted(inc["alerts"], key=lambda x: x["timestamp"])
        timeline_html = f'<div style="border-left:3px solid {accent_color};padding-left:22px;margin:16px 0 20px 8px;">'
        for a in timeline_alerts:
            a_badge = severity_badge(a["severity"])
            timeline_html += (
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
                f'<div style="color:{sub_color};font-size:13px;margin-top:3px;line-height:1.5;">{a["description"]}</div>'
                f'</div>'
            )
        timeline_html += "</div>"
        st.markdown(timeline_html, unsafe_allow_html=True)

        st.markdown("<hr/>", unsafe_allow_html=True)
        section_header("🔍", "Telemetry Evidence Records", "Granular alert evidence for SOC analysts")
        rows = [{
            "Timestamp": a["timestamp"],
            "Vector": a["threat_type"],
            "Severity": a["severity"],
            "Risk Weight": a["risk_score"],
            "Telemetry Notes": a["description"],
        } for a in inc["alerts"]]
        st.dataframe(rows, use_container_width=True, hide_index=True)