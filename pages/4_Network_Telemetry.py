"""ThreatLens — Network Analytics."""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.state import get_data
from utils.ui import (
    inject_css, topbar, section_header, card_row,
    get_chart_theme_config
)

st.set_page_config(page_title="Network Telemetry · ThreatLens", page_icon="📈", layout="wide")

inject_css()
df, alerts, incidents = get_data()

cfg = get_chart_theme_config()

topbar(status_text="TELEMETRY STREAM ANALYTICS ACTIVE", status="good")

section_header("📈", "Deep Network Flow Analytics",
               "Protocol composition, session status ratios, volumetric peaks, and endpoint frequency")

# Quick metric row
total_bytes = int(df["bytes_transferred"].sum())
success_rate = round((df["status"] == "ALLOW").mean() * 100, 1) if "status" in df.columns else 0
unique_srcs = df["source_ip"].nunique()
unique_dsts = df["destination_ip"].nunique()

card_row([
    {"label": "Total Volume",       "value": f"{total_bytes / (1024*1024):.1f} MB", "delta": "Aggregated payload"},
    {"label": "Allow Acceptance",   "value": f"{success_rate}%", "variant": "good" if success_rate > 70 else "warn", "delta": "Policy pass rate"},
    {"label": "Active Source IPs",  "value": f"{unique_srcs:,}", "delta": "Unique initiators"},
    {"label": "Destination Targets","value": f"{unique_dsts:,}", "delta": "Service endpoints"},
])

c1, c2 = st.columns(2)

with c1:
    section_header("🔀", "Protocol Distribution", "Volume proportion across transport protocols")
    proto = df["protocol"].value_counts().reset_index()
    proto.columns = ["protocol", "count"]
    fig_proto = px.pie(
        proto, names="protocol", values="count", hole=0.58,
        color_discrete_sequence=cfg["palette"]
    )
    fig_proto.update_traces(
        textposition="outside",
        textinfo="percent+label",
        marker=dict(line=dict(color=cfg["paper_bgcolor"], width=2))
    )
    fig_proto.update_layout(
        template=cfg["template"],
        paper_bgcolor=cfg["paper_bgcolor"],
        plot_bgcolor=cfg["plot_bgcolor"],
        height=320,
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(color=cfg["font_color"], family="Plus Jakarta Sans, sans-serif"),
        showlegend=False,
    )
    st.plotly_chart(fig_proto, use_container_width=True)

with c2:
    section_header("📊", "Connection Status Breakdown", "Firewall decisions and connection terminations")
    status = df["status"].value_counts().reset_index()
    status.columns = ["status", "count"]
    status_colors = {
        "ALLOW": "#10B981",
        "DENY": "#EF4444",
        "TIMEOUT": "#F59E0B",
        "REJECT": "#DC2626"
    }
    fig_status = px.bar(
        status, x="status", y="count", color="status",
        color_discrete_map=status_colors
    )
    fig_status.update_layout(
        template=cfg["template"],
        paper_bgcolor=cfg["paper_bgcolor"],
        plot_bgcolor=cfg["plot_bgcolor"],
        height=320,
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(gridcolor=cfg["gridcolor"], zerolinecolor=cfg["zerolinecolor"], title="Policy Status"),
        yaxis=dict(gridcolor=cfg["gridcolor"], zerolinecolor=cfg["zerolinecolor"], title="Packet Count"),
        font=dict(color=cfg["font_color"], family="Plus Jakarta Sans, sans-serif"),
    )
    st.plotly_chart(fig_status, use_container_width=True)

section_header("🌐", "Top Source IP Addresses", "Highest-frequency originators within capture window")
top_src = df["source_ip"].value_counts().head(10).reset_index()
top_src.columns = ["source_ip", "count"]
fig_src = px.bar(
    top_src, x="source_ip", y="count",
    color="count", color_continuous_scale=cfg["continuous_blues"]
)
fig_src.update_layout(
    template=cfg["template"],
    paper_bgcolor=cfg["paper_bgcolor"],
    plot_bgcolor=cfg["plot_bgcolor"],
    height=310,
    coloraxis_showscale=False,
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(gridcolor=cfg["gridcolor"], zerolinecolor=cfg["zerolinecolor"], title="Source Address"),
    yaxis=dict(gridcolor=cfg["gridcolor"], zerolinecolor=cfg["zerolinecolor"], title="Flows"),
    font=dict(color=cfg["font_color"], family="Plus Jakarta Sans, sans-serif"),
)
st.plotly_chart(fig_src, use_container_width=True)

section_header("🎯", "Top Target Destination IPs", "Internal & external servers receiving highest connection counts")
top_dst = df["destination_ip"].value_counts().head(10).reset_index()
top_dst.columns = ["destination_ip", "count"]
fig_dst = px.bar(
    top_dst, x="destination_ip", y="count",
    color="count", color_continuous_scale=cfg["continuous_purples"]
)
fig_dst.update_layout(
    template=cfg["template"],
    paper_bgcolor=cfg["paper_bgcolor"],
    plot_bgcolor=cfg["plot_bgcolor"],
    height=310,
    coloraxis_showscale=False,
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(gridcolor=cfg["gridcolor"], zerolinecolor=cfg["zerolinecolor"], title="Destination Address"),
    yaxis=dict(gridcolor=cfg["gridcolor"], zerolinecolor=cfg["zerolinecolor"], title="Flows"),
    font=dict(color=cfg["font_color"], family="Plus Jakarta Sans, sans-serif"),
)
st.plotly_chart(fig_dst, use_container_width=True)

section_header("💾", "Bandwidth & Bytes Transferred Timeline", "Aggregate bandwidth consumption rate per minute")
dft = df.copy()
dft["minute"] = dft["timestamp"].dt.floor("min")
bytes_per_min = dft.groupby("minute")["bytes_transferred"].sum().reset_index()

fig_bytes = px.area(
    bytes_per_min, x="minute", y="bytes_transferred",
    color_discrete_sequence=[cfg["primary_line"]]
)
fig_bytes.update_traces(
    line=dict(width=2.5, color=cfg["primary_line"]),
    fillcolor=cfg["primary_fill"]
)
fig_bytes.update_layout(
    template=cfg["template"],
    paper_bgcolor=cfg["paper_bgcolor"],
    plot_bgcolor=cfg["plot_bgcolor"],
    height=290,
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(gridcolor=cfg["gridcolor"], zerolinecolor=cfg["zerolinecolor"], title=""),
    yaxis=dict(gridcolor=cfg["gridcolor"], zerolinecolor=cfg["zerolinecolor"], title="Bytes / min"),
    font=dict(color=cfg["font_color"], family="Plus Jakarta Sans, sans-serif"),
    hovermode="x unified",
)
st.plotly_chart(fig_bytes, use_container_width=True)