"""ThreatLens — SOC Overview Dashboard."""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.state import get_data
from utils.ui import (
    inject_css, topbar, card_row, section_header,
    severity_badge, get_current_theme, get_chart_theme_config
)

st.set_page_config(page_title="SOC Operations · ThreatLens", page_icon="📊", layout="wide")

inject_css()
df, alerts, incidents = get_data()

theme = get_current_theme()
cfg = get_chart_theme_config()

# Live status in topbar
if incidents:
    topbar(status_text=f"⚠ {len(incidents)} ACTIVE INCIDENT(S)", status="crit")
else:
    topbar(status_text="SYSTEM HEALTHY · ALL SIGNALS NORMAL", status="good")

# ---------- Metrics ----------
total_events = len(df)
total_alerts = len(alerts)
critical = sum(1 for a in alerts if a.get("severity") == "CRITICAL")
avg_risk = int(sum(a.get("risk_score", 0) for a in alerts) / max(total_alerts, 1))

section_header("📊", "Security Operations Overview", "Real-time telemetry and active incident monitoring")

card_row([
    {"label": "Total Events Ingested", "value": f"{total_events:,}", "delta": "Telemetry stream"},
    {"label": "Alerts Triggered",      "value": f"{total_alerts:,}", "variant": "warn" if total_alerts else None, "delta": "Multi-vector"},
    {"label": "Correlated Incidents",  "value": str(len(incidents)), "variant": "crit" if incidents else "good", "delta": "Attacker entities"},
    {"label": "Critical Severity",     "value": str(critical), "variant": "crit" if critical else None, "delta": "Immediate action"},
    {"label": "Average Risk Index",    "value": f"{avg_risk}/100", "delta": "Explainable score"},
])

# ---------- Traffic Over Time ----------
section_header("📈", "Network Activity Over Time", "Event volume timeline across the capture window")

df_chart = df.copy()
df_chart["minute"] = df_chart["timestamp"].dt.floor("min")
traffic = df_chart.groupby("minute").size().reset_index(name="events")

fig_traffic = px.area(traffic, x="minute", y="events", color_discrete_sequence=[cfg["primary_line"]])
fig_traffic.update_traces(
    line=dict(width=2.5, color=cfg["primary_line"]),
    fillcolor=cfg["primary_fill"]
)
fig_traffic.update_layout(
    template=cfg["template"],
    paper_bgcolor=cfg["paper_bgcolor"],
    plot_bgcolor=cfg["plot_bgcolor"],
    height=270,
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(gridcolor=cfg["gridcolor"], zerolinecolor=cfg["zerolinecolor"], title=""),
    yaxis=dict(gridcolor=cfg["gridcolor"], zerolinecolor=cfg["zerolinecolor"], title="Events / min"),
    font=dict(color=cfg["font_color"], family="Plus Jakarta Sans, sans-serif"),
    hovermode="x unified",
)
st.plotly_chart(fig_traffic, use_container_width=True)

# ---------- Distribution + Severity ----------
col1, col2 = st.columns(2)

with col1:
    section_header("🚨", "Threat Distribution", "Frequency by identified attack vector")
    if alerts:
        adf = pd.DataFrame(alerts)
        counts = adf["threat_type"].value_counts().reset_index()
        counts.columns = ["threat_type", "count"]
        fig2 = px.bar(
            counts, x="count", y="threat_type", orientation="h",
            color="count", color_continuous_scale=cfg["continuous_blues"]
        )
        fig2.update_layout(
            template=cfg["template"],
            paper_bgcolor=cfg["paper_bgcolor"],
            plot_bgcolor=cfg["plot_bgcolor"],
            height=320,
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(gridcolor=cfg["gridcolor"], zerolinecolor=cfg["zerolinecolor"], title="Alert Count"),
            yaxis=dict(gridcolor=cfg["gridcolor"], title=""),
            font=dict(color=cfg["font_color"], family="Plus Jakarta Sans, sans-serif"),
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No threat alerts detected in the current window.")

with col2:
    section_header("⚠️", "Severity Breakdown", "Categorization of threat severity levels")
    if alerts:
        adf = pd.DataFrame(alerts)
        sev_counts = adf["severity"].value_counts().reset_index()
        sev_counts.columns = ["severity", "count"]

        fig3 = px.pie(
            sev_counts, names="severity", values="count",
            color="severity", color_discrete_map=cfg["severity_map"],
            hole=0.60
        )
        fig3.update_traces(
            textposition="outside",
            textinfo="percent+label",
            marker=dict(line=dict(color=cfg["paper_bgcolor"], width=2))
        )
        fig3.update_layout(
            template=cfg["template"],
            paper_bgcolor=cfg["paper_bgcolor"],
            plot_bgcolor=cfg["plot_bgcolor"],
            height=320,
            margin=dict(l=10, r=10, t=10, b=10),
            font=dict(color=cfg["font_color"], family="Plus Jakarta Sans, sans-serif"),
            showlegend=False,
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No threats detected.")

# ---------- Recent Incidents ----------
section_header("🔥", "High-Priority Correlated Incidents", "Aggregated threats mapped to unique attacker IPs")

sub_color = "#64748B" if theme == "light" else "#94A3B8"
title_color = "#0F172A" if theme == "light" else "#F8FAFC"
score_crit_color = "#DC2626" if theme == "light" else "#FF6688"

if incidents:
    for inc in incidents[:4]:
        badge = severity_badge(inc["severity"])
        st.markdown(f"""
        <div class="tl-card" style="margin-bottom:12px;">
          <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;">
            <div>
              <div style="font-size:17px;font-weight:700;color:{title_color};letter-spacing:-0.2px;">
                {inc['title']}
              </div>
              <div style="font-size:13px;color:{sub_color};margin-top:6px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
                <span>Source: <code>{inc['source_ip']}</code></span>
                <span>•</span>
                <span>{inc['first_seen']} → {inc['last_seen']}</span>
                <span>•</span>
                <span><b>{inc['alert_count']}</b> alerts</span>
                <span>•</span>
                <span><b>{len(inc['threat_types'])}</b> threat classes</span>
              </div>
            </div>
            <div style="text-align:right;display:flex;flex-direction:column;align-items:flex-end;">
              {badge}
              <div style="font-size:24px;font-weight:800;color:{score_crit_color};margin-top:4px;">
                {inc['risk_score']}<span style="font-size:13px;font-weight:600;color:{sub_color};">/100</span>
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No incidents detected. Head to **Intrusion Scanner** in the sidebar to run the intrusion detection scenario.")