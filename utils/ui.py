"""ThreatLens — High-Vibrancy Dual-Theme UI System (Vibrant Light & Neon Cyber)."""

import streamlit as st


def get_current_theme() -> str:
    """Return active theme: 'light' (default) or 'cyber', synced with query_params and session_state."""
    if hasattr(st, "query_params") and "theme" in st.query_params:
        param = st.query_params.get("theme")
        if param in ["light", "cyber"]:
            st.session_state["theme"] = param

    if "theme" not in st.session_state:
        st.session_state["theme"] = "light"
    return st.session_state["theme"]


def render_sidebar_header():
    """Renders logo, title, status chip, and guaranteed navigation links with icons at top of sidebar."""
    theme = get_current_theme()
    title_gradient = (
        "linear-gradient(135deg, #3730A3 0%, #4F46E5 50%, #0284C7 100%)"
        if theme == "light"
        else "linear-gradient(135deg, #00F2FE 0%, #818CF8 50%, #C084FC 100%)"
    )
    sub_color = "#64748B" if theme == "light" else "#94A3B8"
    border_color = "#E2E8F0" if theme == "light" else "rgba(0, 242, 254, 0.2)"
    badge_bg = "rgba(79, 70, 229, 0.08)" if theme == "light" else "rgba(0, 242, 254, 0.12)"
    badge_color = "#4F46E5" if theme == "light" else "#00F2FE"

    # 1. Logo & Brand Title at the beginning of the sidebar
    st.sidebar.markdown(f"""
    <div style="padding: 2px 2px 8px 2px; margin-bottom: 6px; border-bottom: 1px solid {border_color};">
      <div style="display: flex; align-items: center; gap: 7px;">
        <span style="font-size: 22px; filter: drop-shadow(0 2px 5px rgba(79,70,229,0.3));">🛡️</span>
        <div>
          <div style="font-family:'Outfit','Plus Jakarta Sans',sans-serif;font-size:16px;font-weight:800;background:{title_gradient};-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:-0.3px;line-height:1.15;">
            ThreatLens
          </div>
          <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:8.5px;font-weight:700;color:{sub_color};letter-spacing:0.8px;text-transform:uppercase;margin-top:1px;">
            Security Platform
          </div>
        </div>
      </div>
      <div style="margin-top: 6px; display: flex; align-items: center; justify-content: space-between;">
        <span style="display:inline-flex;align-items:center;gap:3px;padding:2px 5px;border-radius:999px;background:{badge_bg};color:{badge_color};font-size:8.5px;font-weight:800;letter-spacing:0.6px;">
          <span style="width:4px;height:4px;border-radius:50%;background:{badge_color};display:inline-block;"></span>
          LIVE SHIELD
        </span>
        <span style="font-family:'JetBrains Mono',monospace;font-size:8.5px;color:{sub_color};font-weight:600;">v2.4.0</span>
      </div>
    </div>
    <div style="font-size: 8.5px; font-weight: 800; color: {sub_color}; text-transform: uppercase; letter-spacing: 0.8px; margin: 4px 2px 4px 2px;">
      Services &amp; Navigation
    </div>
    """, unsafe_allow_html=True)

    # 2. Navigation items with icons
    st.sidebar.page_link("app.py", label="Home Overview", icon="🏠")
    st.sidebar.page_link("pages/1_SOC_Operations.py", label="SOC Operations", icon="📊")
    st.sidebar.page_link("pages/2_Intrusion_Scanner.py", label="Intrusion Scanner", icon="🚀")
    st.sidebar.page_link("pages/3_Active_Incidents.py", label="Active Incidents", icon="🚨")
    st.sidebar.page_link("pages/4_Network_Telemetry.py", label="Network Telemetry", icon="📈")
    st.sidebar.page_link("pages/5_Entity_Forensics.py", label="Entity Forensics", icon="🔎")

    # 3. Sidebar footer
    st.sidebar.markdown(f"""
    <div style="margin-top: 20px; padding: 10px 4px; border-top: 1px solid {border_color}; font-size: 10px; color: {sub_color}; line-height: 1.4;">
      🛡️ <b>Defensive Triage Engine</b><br/>
      Threat Telemetry Analytics
    </div>
    """, unsafe_allow_html=True)


def get_theme_css(theme: str) -> str:
    """Generate dynamic CSS based on active theme."""
    if theme == "light":
        return """
        /* ☀️ VIBRANT LIGHT THEME */
        :root {
            --tl-bg: #F8FAFC;
            --tl-surface: #FFFFFF;
            --tl-surface-elevated: #FFFFFF;
            --tl-border: #E2E8F0;
            --tl-border-hover: #6366F1;
            --tl-text-main: #0F172A;
            --tl-text-muted: #64748B;
            --tl-text-subtle: #94A3B8;
            --tl-primary: #4F46E5;
            --tl-primary-glow: rgba(79, 70, 229, 0.25);
            --tl-accent-cyan: #0284C7;
            --tl-accent-green: #059669;
            --tl-accent-amber: #D97706;
            --tl-accent-red: #DC2626;
            --tl-card-shadow: 0 2px 12px -2px rgba(15, 23, 42, 0.05), 0 1px 3px rgba(15, 23, 42, 0.03);
            --tl-card-shadow-hover: 0 8px 22px -3px rgba(99, 102, 241, 0.15), 0 3px 6px rgba(15, 23, 42, 0.04);
        }

        .stApp {
            background:
              radial-gradient(1200px 600px at 85% -5%, rgba(99, 102, 241, 0.12), transparent 60%),
              radial-gradient(1000px 500px at -5% 105%, rgba(14, 165, 233, 0.12), transparent 60%),
              radial-gradient(800px 400px at 50% 50%, rgba(244, 63, 94, 0.04), transparent 60%),
              #F8FAFC !important;
            color: #0F172A !important;
        }

        /* Slimmer 180px Sidebar */
        section[data-testid="stSidebar"] {
            width: 180px !important;
            min-width: 180px !important;
            max-width: 180px !important;
            background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%) !important;
            border-right: 1px solid #E2E8F0 !important;
            box-shadow: 4px 0 20px rgba(15, 23, 42, 0.03) !important;
            backdrop-filter: blur(14px) !important;
        }
        div[data-testid="stSidebarContent"] {
            width: 180px !important;
            padding: 0.4rem 0.25rem !important;
        }
        section[data-testid="stSidebar"] * {
            color: #334155 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        section[data-testid="stSidebar"] a {
            color: #475569 !important;
            font-size: 11.5px !important;
            font-weight: 600 !important;
            border-radius: 7px !important;
            padding: 5px 6px !important;
            margin: 2px 0 !important;
            transition: all 0.18s ease !important;
        }
        section[data-testid="stSidebar"] a:hover {
            color: #4F46E5 !important;
            background: rgba(79, 70, 229, 0.08) !important;
            transform: translateX(2px) !important;
        }
        section[data-testid="stSidebar"] a:hover * { color: #4F46E5 !important; }
        section[data-testid="stSidebar"] a[aria-current="page"] {
            background: linear-gradient(135deg, rgba(79, 70, 229, 0.12) 0%, rgba(6, 182, 212, 0.08) 100%) !important;
            border-left: 3px solid #4F46E5 !important;
            color: #4338CA !important;
            font-weight: 700 !important;
        }
        section[data-testid="stSidebar"] a[aria-current="page"] * {
            color: #4338CA !important;
            font-weight: 700 !important;
        }

        h1, h2, h3, h4 {
            color: #0F172A !important;
            font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.025em;
        }
        h1 {
            background: linear-gradient(135deg, #3730A3 0%, #4F46E5 40%, #0284C7 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
        }

        .tl-topbar {
            display: flex; align-items: center; justify-content: space-between;
            padding: 12px 20px; margin: -8px 0 18px 0;
            background: #FFFFFF;
            border: 1px solid #E2E8F0; border-radius: 14px;
            box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.05);
        }
        .tl-brand-name {
            font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
            font-size: 21px; font-weight: 800;
            background: linear-gradient(135deg, #3730A3 0%, #0284C7 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            letter-spacing: -0.4px;
        }
        .tl-brand-sub { font-size: 11px; font-weight: 600; color: #64748B; letter-spacing: 0.6px; }

        .tl-card {
            position: relative; padding: 16px 18px;
            background: #FFFFFF;
            border: 1px solid #E2E8F0; border-radius: 12px;
            box-shadow: var(--tl-card-shadow);
            overflow: hidden;
            transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s ease, border-color 0.2s ease;
        }
        .tl-card:hover {
            transform: translateY(-2px);
            border-color: #6366F1;
            box-shadow: var(--tl-card-shadow-hover);
        }
        .tl-card::before {
            content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
            background: linear-gradient(180deg, #4F46E5 0%, #06B6D4 100%);
            border-radius: 4px 0 0 4px;
        }
        .tl-card-label {
            font-size: 11px; text-transform: uppercase;
            letter-spacing: 1.1px; font-weight: 700; color: #64748B; margin-bottom: 4px;
        }
        .tl-card-value {
            font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
            font-size: 26px; font-weight: 800; color: #0F172A; line-height: 1.15;
        }
        .tl-card-delta { font-size: 12px; font-weight: 600; color: #059669; margin-top: 4px; }
        .tl-card.crit::before { background: linear-gradient(180deg, #EF4444 0%, #DC2626 100%); }
        .tl-card.crit .tl-card-value { color: #DC2626; }
        .tl-card.warn::before { background: linear-gradient(180deg, #F59E0B 0%, #D97706 100%); }
        .tl-card.warn .tl-card-value { color: #D97706; }
        .tl-card.good::before { background: linear-gradient(180deg, #10B981 0%, #059669 100%); }
        .tl-card.good .tl-card-value { color: #059669; }

        .stButton > button {
            background: linear-gradient(135deg, #4F46E5 0%, #06B6D4 100%) !important;
            color: #FFFFFF !important; border: none !important;
            border-radius: 10px !important; padding: 0.55rem 1.3rem !important;
            font-weight: 600 !important; font-size: 13.5px !important;
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 22px rgba(79, 70, 229, 0.4) !important;
            filter: brightness(1.05) !important;
        }
        .stButton > button:active { transform: translateY(0) !important; }

        div[data-testid="stAlert"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-left: 4px solid #4F46E5 !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04) !important;
            color: #0F172A !important;
        }
        div[data-testid="stAlert"] * { color: #0F172A !important; }

        .stDataFrame {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04) !important;
            overflow: hidden;
        }

        div[data-testid="stMetricValue"] { color: #0F172A !important; font-weight: 800 !important; }
        div[data-testid="stMetricLabel"] {
            color: #64748B !important; text-transform: uppercase;
            font-size: 11px !important; letter-spacing: 1px; font-weight: 700 !important;
        }
        hr { border-color: #E2E8F0 !important; margin: 20px 0 !important; }
        code {
            background: #EEF2F6 !important;
            color: #4338CA !important;
            border-radius: 6px !important;
            padding: 2px 6px !important;
            font-weight: 600 !important;
        }
        """

    else:
        return """
        /* ⚡ NEON CYBER THEME */
        :root {
            --tl-bg: #0B0F19;
            --tl-surface: rgba(20, 27, 46, 0.85);
            --tl-surface-elevated: rgba(27, 36, 61, 0.9);
            --tl-border: rgba(0, 242, 254, 0.22);
            --tl-border-hover: #00F2FE;
            --tl-text-main: #F8FAFC;
            --tl-text-muted: #94A3B8;
            --tl-text-subtle: #64748B;
            --tl-primary: #00F2FE;
            --tl-primary-glow: rgba(0, 242, 254, 0.35);
            --tl-accent-cyan: #00F2FE;
            --tl-accent-green: #10E7A0;
            --tl-accent-amber: #FBBF24;
            --tl-accent-red: #FF3366;
            --tl-card-shadow: 0 6px 24px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.06);
            --tl-card-shadow-hover: 0 0 22px rgba(0, 242, 254, 0.32), 0 10px 24px rgba(0, 0, 0, 0.55);
        }

        .stApp {
            background:
              radial-gradient(1200px 600px at 85% -10%, rgba(0, 242, 254, 0.16), transparent 60%),
              radial-gradient(1000px 500px at -10% 105%, rgba(168, 85, 247, 0.16), transparent 60%),
              radial-gradient(800px 400px at 50% 50%, rgba(16, 231, 160, 0.06), transparent 60%),
              #0B0F19 !important;
            color: #F8FAFC !important;
        }

        /* Slimmer 180px Sidebar */
        section[data-testid="stSidebar"] {
            width: 180px !important;
            min-width: 180px !important;
            max-width: 180px !important;
            background: linear-gradient(180deg, #111827 0%, #0B0F19 100%) !important;
            border-right: 1px solid rgba(0, 242, 254, 0.22) !important;
            box-shadow: 4px 0 20px rgba(0, 0, 0, 0.5) !important;
            backdrop-filter: blur(14px) !important;
        }
        div[data-testid="stSidebarContent"] {
            width: 180px !important;
            padding: 0.4rem 0.25rem !important;
        }
        section[data-testid="stSidebar"] * {
            color: #E2E8F0 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        section[data-testid="stSidebar"] a {
            color: #94A3B8 !important;
            font-size: 11.5px !important;
            font-weight: 600 !important;
            border-radius: 7px !important;
            padding: 5px 6px !important;
            margin: 2px 0 !important;
            transition: all 0.18s ease !important;
        }
        section[data-testid="stSidebar"] a:hover {
            color: #00F2FE !important;
            background: rgba(0, 242, 254, 0.1) !important;
            transform: translateX(2px) !important;
        }
        section[data-testid="stSidebar"] a:hover * { color: #00F2FE !important; }
        section[data-testid="stSidebar"] a[aria-current="page"] {
            background: linear-gradient(135deg, rgba(0, 242, 254, 0.20) 0%, rgba(168, 85, 247, 0.12) 100%) !important;
            border-left: 3px solid #00F2FE !important;
            color: #00F2FE !important;
            font-weight: 700 !important;
            box-shadow: 0 0 14px rgba(0, 242, 254, 0.22) !important;
        }
        section[data-testid="stSidebar"] a[aria-current="page"] * {
            color: #00F2FE !important;
            font-weight: 700 !important;
        }

        h1, h2, h3, h4 {
            color: #F8FAFC !important;
            font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.025em;
        }
        h1 {
            background: linear-gradient(135deg, #00F2FE 0%, #818CF8 50%, #C084FC 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            filter: drop-shadow(0 0 12px rgba(0, 242, 254, 0.35));
        }

        .tl-topbar {
            display: flex; align-items: center; justify-content: space-between;
            padding: 12px 20px; margin: -8px 0 18px 0;
            background: linear-gradient(135deg, rgba(20, 27, 46, 0.92), rgba(11, 15, 25, 0.92));
            border: 1px solid rgba(0, 242, 254, 0.25); border-radius: 14px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), 0 0 15px rgba(0, 242, 254, 0.1);
        }
        .tl-brand-name {
            font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
            font-size: 21px; font-weight: 800;
            background: linear-gradient(135deg, #00F2FE 0%, #C084FC 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            letter-spacing: -0.4px;
            filter: drop-shadow(0 0 10px rgba(0, 242, 254, 0.4));
        }
        .tl-brand-sub { font-size: 11px; font-weight: 600; color: #94A3B8; letter-spacing: 0.6px; }

        .tl-card {
            position: relative; padding: 16px 18px;
            background: linear-gradient(180deg, rgba(20, 27, 46, 0.85) 0%, rgba(14, 20, 36, 0.85) 100%);
            border: 1px solid rgba(0, 242, 254, 0.22); border-radius: 12px;
            backdrop-filter: blur(12px);
            box-shadow: var(--tl-card-shadow);
            overflow: hidden;
            transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s ease, border-color 0.2s ease;
        }
        .tl-card:hover {
            transform: translateY(-2px);
            border-color: #00F2FE;
            box-shadow: var(--tl-card-shadow-hover);
        }
        .tl-card::before {
            content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
            background: linear-gradient(180deg, #00F2FE 0%, #A855F7 100%);
            border-radius: 4px 0 0 4px;
            box-shadow: 0 0 10px rgba(0, 242, 254, 0.6);
        }
        .tl-card-label {
            font-size: 11px; text-transform: uppercase;
            letter-spacing: 1.1px; font-weight: 700; color: #94A3B8; margin-bottom: 4px;
        }
        .tl-card-value {
            font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
            font-size: 26px; font-weight: 800; color: #F8FAFC; line-height: 1.15;
        }
        .tl-card-delta { font-size: 12px; font-weight: 600; color: #10E7A0; margin-top: 4px; }
        .tl-card.crit::before {
            background: linear-gradient(180deg, #FF3366 0%, #E11D48 100%);
            box-shadow: 0 0 12px rgba(255, 51, 102, 0.7);
        }
        .tl-card.crit .tl-card-value {
            color: #FF6688;
            text-shadow: 0 0 10px rgba(255, 51, 102, 0.4);
        }
        .tl-card.warn::before {
            background: linear-gradient(180deg, #FBBF24 0%, #F59E0B 100%);
            box-shadow: 0 0 10px rgba(251, 191, 36, 0.6);
        }
        .tl-card.warn .tl-card-value { color: #FBBF24; }
        .tl-card.good::before {
            background: linear-gradient(180deg, #10E7A0 0%, #059669 100%);
            box-shadow: 0 0 10px rgba(16, 231, 160, 0.6);
        }
        .tl-card.good .tl-card-value { color: #10E7A0; }

        .stButton > button {
            background: linear-gradient(135deg, #00F2FE 0%, #7F00FF 100%) !important;
            color: #FFFFFF !important; border: none !important;
            border-radius: 10px !important; padding: 0.55rem 1.3rem !important;
            font-weight: 600 !important; font-size: 13.5px !important;
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.35) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 0 30px rgba(0, 242, 254, 0.65) !important;
            filter: brightness(1.1) !important;
        }
        .stButton > button:active { transform: translateY(0) !important; }

        div[data-testid="stAlert"] {
            background-color: rgba(20, 27, 46, 0.85) !important;
            border: 1px solid rgba(0, 242, 254, 0.25) !important;
            border-left: 4px solid #00F2FE !important;
            border-radius: 12px !important;
            color: #F8FAFC !important;
        }
        div[data-testid="stAlert"] * { color: #F8FAFC !important; }

        .stDataFrame {
            background: rgba(20, 27, 46, 0.8) !important;
            border: 1px solid rgba(0, 242, 254, 0.25) !important;
            border-radius: 12px !important;
            overflow: hidden;
        }

        div[data-testid="stMetricValue"] { color: #F8FAFC !important; font-weight: 800 !important; }
        div[data-testid="stMetricLabel"] {
            color: #94A3B8 !important; text-transform: uppercase;
            font-size: 11px !important; letter-spacing: 1px; font-weight: 700 !important;
        }
        hr { border-color: rgba(0, 242, 254, 0.18) !important; margin: 20px 0 !important; }
        code {
            background: rgba(0, 242, 254, 0.12) !important;
            color: #00F2FE !important;
            border: 1px solid rgba(0, 242, 254, 0.25) !important;
            border-radius: 6px !important;
            padding: 2px 6px !important;
            font-weight: 600 !important;
        }
        """


SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

button[data-testid="stSidebarCollapseButton"],
div[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarHeader"] > button {
    display: none !important;
}

@keyframes tl-pulse-ring {
    0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { transform: scale(1.05); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
    100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

@keyframes tl-crit-ring {
    0% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
    70% { transform: scale(1.05); box-shadow: 0 0 0 8px rgba(239, 68, 68, 0); }
    100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

.tl-brand { display: flex; align-items: center; gap: 14px; }
.tl-brand-logo {
    font-size: 30px;
    filter: drop-shadow(0 2px 8px rgba(99, 102, 241, 0.35));
    transition: transform 0.2s ease;
}
.tl-brand-logo:hover { transform: scale(1.1) rotate(4deg); }

.tl-status {
    display: flex; align-items: center; gap: 8px;
    padding: 6px 14px; border-radius: 999px;
    font-size: 11px; font-weight: 700; letter-spacing: 0.5px;
}
.tl-status-dot {
    width: 8px; height: 8px; border-radius: 50%;
    animation: tl-pulse-ring 2s infinite cubic-bezier(0.4, 0, 0.6, 1);
}
.tl-status-dot.crit {
    animation: tl-crit-ring 1.5s infinite cubic-bezier(0.4, 0, 0.6, 1);
}

/* Theme toggle button in topbar */
.tl-theme-toggle {
    display: inline-flex; align-items: center; justify-content: center;
    width: 36px; height: 36px; border-radius: 50%;
    font-size: 18px; text-decoration: none !important;
    background: var(--tl-surface);
    border: 1px solid var(--tl-border);
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
}
.tl-theme-toggle:hover {
    transform: scale(1.15) rotate(15deg);
    border-color: var(--tl-border-hover);
    box-shadow: 0 4px 14px var(--tl-primary-glow);
}

/* Floating top-right corner theme toggle symbol */
.tl-corner-theme-toggle {
    position: fixed;
    top: 14px;
    right: 18px;
    z-index: 999999;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 16px;
    font-weight: 700;
    text-decoration: none !important;
    color: var(--tl-text-main) !important;
    background: var(--tl-surface);
    border: 1px solid var(--tl-border);
    box-shadow: 0 4px 18px rgba(0,0,0,0.12);
    backdrop-filter: blur(12px);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.tl-corner-theme-toggle:hover {
    transform: translateY(-2px) scale(1.05);
    border-color: var(--tl-border-hover);
    box-shadow: 0 6px 22px var(--tl-primary-glow);
}

.tl-cards {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 14px; margin: 12px 0 20px 0;
}

/* ==================================================== */
/* COMPACT EXPANDABLE SERVICE CARDS (Exact Screenshot Size) */
/* ==================================================== */
details.tl-service-card-expander {
    position: relative;
    background: var(--tl-surface);
    border: 1px solid var(--tl-border);
    border-radius: 12px;
    box-shadow: var(--tl-card-shadow);
    overflow: hidden;
    transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 12px;
}
details.tl-service-card-expander:hover {
    border-color: var(--tl-border-hover);
    box-shadow: var(--tl-card-shadow-hover);
    transform: translateY(-2px);
}
details.tl-service-card-expander[open] {
    border-color: var(--tl-border-hover);
    box-shadow: var(--tl-card-shadow-hover);
    transform: none;
}
details.tl-service-card-expander::before {
    content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
    background: linear-gradient(180deg, var(--tl-primary) 0%, var(--tl-accent-cyan) 100%);
    border-radius: 4px 0 0 4px;
}
summary.tl-service-card-summary {
    padding: 14px 16px;
    cursor: pointer;
    user-select: none;
    list-style: none !important;
    display: flex;
    flex-direction: column;
    gap: 4px;
    transition: background 0.15s ease;
}
summary.tl-service-card-summary::-webkit-details-marker {
    display: none !important;
}
summary.tl-service-card-summary:hover {
    background: rgba(99, 102, 241, 0.04);
}
.tl-card-top-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.tl-card-badge-pill {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 5px;
    font-size: 9.5px;
    font-weight: 800;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}
.tl-card-toggle-icon {
    font-size: 11px;
    font-weight: 700;
    color: var(--tl-primary);
    transition: transform 0.25s ease;
}
details[open] .tl-card-toggle-icon {
    transform: rotate(180deg);
}
.tl-card-main-title {
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
    font-size: 16.5px;
    font-weight: 800;
    color: var(--tl-text-main);
    margin-top: 3px;
    letter-spacing: -0.2px;
}
.tl-card-short-desc {
    font-size: 12px;
    color: var(--tl-text-muted);
    line-height: 1.45;
    margin-top: 4px;
}
.tl-card-expanded-body {
    padding: 12px 16px 16px 16px;
    border-top: 1px solid var(--tl-border);
    background: rgba(0, 0, 0, 0.015);
}
.tl-card-expanded-text {
    font-size: 12.5px;
    color: var(--tl-text-muted);
    line-height: 1.5;
    margin-bottom: 10px;
}
.tl-card-bullets-list {
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin-bottom: 12px;
}
.tl-card-bullet-row {
    font-size: 11.5px;
    font-weight: 600;
    color: var(--tl-text-main);
    display: flex;
    align-items: center;
    gap: 6px;
}
.tl-card-launch-button {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 7px;
    font-size: 12px;
    font-weight: 700;
    text-decoration: none !important;
    background: linear-gradient(135deg, var(--tl-primary) 0%, var(--tl-accent-cyan) 100%);
    color: #FFFFFF !important;
    box-shadow: 0 3px 10px var(--tl-primary-glow);
    transition: all 0.2s ease;
}
.tl-card-launch-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 5px 14px var(--tl-primary-glow);
    filter: brightness(1.08);
}

/* Hero Section */
.tl-hero {
    text-align: center;
    padding: 24px 16px 10px 16px;
    position: relative;
}
.tl-hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 12px; border-radius: 999px;
    font-size: 10.5px; font-weight: 700; letter-spacing: 1px;
    text-transform: uppercase; margin-bottom: 8px;
}
.tl-hero-title {
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif;
    font-size: 40px; font-weight: 900; letter-spacing: -0.03em;
    margin: 4px 0 6px 0;
}
.tl-hero-subtitle {
    font-size: 14px; font-weight: 500;
    max-width: 650px; margin: 0 auto; line-height: 1.55;
}
</style>
"""


def _clean(html: str) -> str:
    """Collapse whitespace so Streamlit's markdown parser treats it as raw HTML."""
    return "".join(line.strip() for line in html.splitlines())


def inject_css():
    """Inject full theme CSS, sidebar brand header with icons, and corner theme toggle symbol."""
    theme = get_current_theme()
    theme_css = get_theme_css(theme)
    full_css = f"{SHARED_CSS}\n<style>{theme_css}</style>"
    st.markdown(full_css, unsafe_allow_html=True)

    # Render floating top-right theme toggle symbol
    next_theme = "cyber" if theme == "light" else "light"
    next_symbol = "🌙" if theme == "light" else "☀️"
    next_label = "Dark" if theme == "light" else "Light"
    next_title = "Switch to Dark / Neon Cyber Mode" if theme == "light" else "Switch to Bright Light Mode"

    st.markdown(f"""
    <a href="?theme={next_theme}" target="_self" class="tl-corner-theme-toggle" title="{next_title}">
      <span>{next_symbol}</span>
      <span style="font-size:12px;letter-spacing:0.3px;">{next_label}</span>
    </a>
    """, unsafe_allow_html=True)

    # Render custom sidebar with logo at the beginning and clean icon navigation
    render_sidebar_header()


def topbar(status_text: str = "SYSTEM NORMAL", status: str = "good"):
    """Theme-aware Topbar with status badge and theme toggle symbol."""
    theme = get_current_theme()
    next_theme = "cyber" if theme == "light" else "light"
    next_symbol = "🌙" if theme == "light" else "☀️"
    next_title = "Switch to Dark / Neon Cyber Mode" if theme == "light" else "Switch to Bright Light Mode"

    if theme == "light":
        colors = {
            "good": {"color": "#059669", "bg": "#ECFDF5", "border": "#A7F3D0", "dot": "#10B981"},
            "warn": {"color": "#D97706", "bg": "#FFFBEB", "border": "#FDE68A", "dot": "#F59E0B"},
            "crit": {"color": "#DC2626", "bg": "#FEF2F2", "border": "#FECACA", "dot": "#EF4444"},
        }
    else:
        colors = {
            "good": {"color": "#10E7A0", "bg": "rgba(16,231,160,0.12)", "border": "rgba(16,231,160,0.35)", "dot": "#10E7A0"},
            "warn": {"color": "#FBBF24", "bg": "rgba(251,191,36,0.12)", "border": "rgba(251,191,36,0.35)", "dot": "#FBBF24"},
            "crit": {"color": "#FF3366", "bg": "rgba(255,51,102,0.15)", "border": "rgba(255,51,102,0.45)", "dot": "#FF3366"},
        }

    c = colors.get(status, colors["good"])
    dot_crit_cls = " crit" if status == "crit" else ""

    html = _clean(f"""
    <div class="tl-topbar">
      <div class="tl-brand">
        <div class="tl-brand-logo">🛡️</div>
        <div>
          <div class="tl-brand-name">ThreatLens</div>
          <div class="tl-brand-sub">ENTERPRISE NETWORK SECURITY &amp; INTRUSION INVESTIGATION</div>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:12px;">
        <div class="tl-status" style="color:{c['color']};background:{c['bg']};border:1px solid {c['border']};">
          <div class="tl-status-dot{dot_crit_cls}" style="background:{c['dot']};"></div>
          {status_text}
        </div>
        <a href="?theme={next_theme}" target="_self" class="tl-theme-toggle" title="{next_title}">
          {next_symbol}
        </a>
      </div>
    </div>
    """)
    st.markdown(html, unsafe_allow_html=True)


def card_row(cards: list):
    """cards = list of {label, value, delta?, variant?}"""
    html = '<div class="tl-cards">'
    for c in cards:
        variant = f' {c["variant"]}' if c.get("variant") else ""
        delta = f'<div class="tl-card-delta">{c["delta"]}</div>' if c.get("delta") else ""
        html += (
            f'<div class="tl-card{variant}">'
            f'<div class="tl-card-label">{c["label"]}</div>'
            f'<div class="tl-card-value">{c["value"]}</div>'
            f'{delta}'
            f'</div>'
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def section_header(icon: str, title: str, subtitle: str = ""):
    """Sleek section header with theme-appropriate subtext."""
    theme = get_current_theme()
    sub_color = "#64748B" if theme == "light" else "#94A3B8"
    title_color = "#0F172A" if theme == "light" else "#F8FAFC"

    sub = (f'<div style="font-size:12.5px;color:{sub_color};margin-top:2px;font-weight:500;">{subtitle}</div>'
           if subtitle else "")
    html = _clean(f"""
    <div style="margin:18px 0 10px 0;">
      <div style="font-family:'Outfit','Plus Jakarta Sans',sans-serif;font-size:18px;font-weight:700;color:{title_color};display:flex;align-items:center;gap:8px;">
        <span style="font-size:20px;">{icon}</span> <span>{title}</span>
      </div>
      {sub}
    </div>
    """)
    st.markdown(html, unsafe_allow_html=True)


def severity_badge(sev: str) -> str:
    """Returns a vibrant, modern badge for severity tags."""
    theme = get_current_theme()
    if theme == "light":
        palettes = {
            "LOW": {"color": "#059669", "bg": "#ECFDF5", "border": "#A7F3D0"},
            "MEDIUM": {"color": "#D97706", "bg": "#FFFBEB", "border": "#FDE68A"},
            "HIGH": {"color": "#EA580C", "bg": "#FFF7ED", "border": "#FFEDD5"},
            "CRITICAL": {"color": "#DC2626", "bg": "#FEF2F2", "border": "#FECACA"},
        }
    else:
        palettes = {
            "LOW": {"color": "#10E7A0", "bg": "rgba(16,231,160,0.14)", "border": "rgba(16,231,160,0.4)"},
            "MEDIUM": {"color": "#FBBF24", "bg": "rgba(251,191,36,0.14)", "border": "rgba(251,191,36,0.4)"},
            "HIGH": {"color": "#FB7185", "bg": "rgba(251,113,133,0.15)", "border": "rgba(251,113,133,0.45)"},
            "CRITICAL": {"color": "#FF3366", "bg": "rgba(255,51,102,0.18)", "border": "rgba(255,51,102,0.5)"},
        }

    p = palettes.get(sev, {"color": "#64748B", "bg": "#F1F5F9", "border": "#CBD5E1"})
    return (
        f'<span style="display:inline-block;padding:3px 12px;border-radius:999px;'
        f'background:{p["bg"]};border:1px solid {p["border"]};color:{p["color"]};font-size:11px;'
        f'font-weight:700;letter-spacing:0.5px;text-transform:uppercase;">{sev}</span>'
    )


def metric_card(label: str, value: str, delta: str = "",
                variant: str = "", icon: str = "") -> str:
    """Return a single-card HTML string for use inline."""
    variant_cls = f" {variant}" if variant else ""
    icon_html = f'<span style="margin-right:8px;">{icon}</span>' if icon else ""
    delta_html = f'<div class="tl-card-delta">{delta}</div>' if delta else ""
    return (
        f'<div class="tl-card{variant_cls}">'
        f'<div class="tl-card-label">{icon_html}{label}</div>'
        f'<div class="tl-card-value">{value}</div>'
        f'{delta_html}'
        f'</div>'
    )


def walkthrough_card(phase: str, title: str, description: str, link_url: str = None) -> str:
    """Renders a card matching the exact visual style and proportions in the screenshot."""
    theme = get_current_theme()
    badge_bg = "rgba(79, 70, 229, 0.08)" if theme == "light" else "rgba(0, 242, 254, 0.12)"
    badge_color = "#4F46E5" if theme == "light" else "#00F2FE"
    badge_border = "rgba(79, 70, 229, 0.2)" if theme == "light" else "rgba(0, 242, 254, 0.3)"
    title_color = "#0F172A" if theme == "light" else "#F8FAFC"
    sub_color = "#64748B" if theme == "light" else "#94A3B8"

    card_inner = f"""
    <div class="tl-card" style="min-height:106px;padding:14px 16px;cursor:{'pointer' if link_url else 'default'};">
      <div style="margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;">
        <span style="display:inline-block;padding:2px 8px;border-radius:6px;background:{badge_bg};border:1px solid {badge_border};color:{badge_color};font-size:9.5px;font-weight:800;letter-spacing:0.8px;text-transform:uppercase;">
          {phase}
        </span>
        {f'<span style="font-size:11px;color:{badge_color};font-weight:700;">Open →</span>' if link_url else ''}
      </div>
      <div style="font-family:'Outfit','Plus Jakarta Sans',sans-serif;font-size:16px;font-weight:800;color:{title_color};letter-spacing:-0.2px;line-height:1.2;margin-bottom:5px;">
        {title}
      </div>
      <div style="font-size:12px;color:{sub_color};line-height:1.45;">
        {description}
      </div>
    </div>
    """

    if link_url:
        return _clean(f'<a href="{link_url}" target="_self" style="text-decoration:none !important;color:inherit !important;display:block;">{card_inner}</a>')
    return _clean(card_inner)


def expandable_service_card(badge: str, title: str, short_desc: str, full_desc: str,
                            bullets: list, link_url: str, link_label: str = "Launch Service →") -> str:
    """Renders a compact card matching screenshot dimensions that expands/collapses on click."""
    theme = get_current_theme()
    badge_bg = "rgba(79, 70, 229, 0.08)" if theme == "light" else "rgba(0, 242, 254, 0.12)"
    badge_color = "#4F46E5" if theme == "light" else "#00F2FE"
    badge_border = "rgba(79, 70, 229, 0.2)" if theme == "light" else "rgba(0, 242, 254, 0.3)"
    title_color = "#0F172A" if theme == "light" else "#F8FAFC"
    sub_color = "#64748B" if theme == "light" else "#94A3B8"

    bullet_items = "".join(
        f'<div class="tl-card-bullet-row"><span>{b}</span></div>'
        for b in bullets
    )

    return _clean(f"""
    <details class="tl-service-card-expander">
      <summary class="tl-service-card-summary">
        <div class="tl-card-top-row">
          <span class="tl-card-badge-pill" style="background:{badge_bg};border:1px solid {badge_border};color:{badge_color};">
            {badge}
          </span>
          <span class="tl-card-toggle-icon">▾</span>
        </div>
        <div class="tl-card-main-title" style="color:{title_color};">{title}</div>
        <div class="tl-card-short-desc" style="color:{sub_color};">{short_desc}</div>
      </summary>
      <div class="tl-card-expanded-body">
        <div class="tl-card-expanded-text" style="color:{sub_color};">{full_desc}</div>
        <div class="tl-card-bullets-list">
          {bullet_items}
        </div>
        <div style="margin-top:10px;">
          <a href="{link_url}" target="_self" class="tl-card-launch-button">
            {link_label}
          </a>
        </div>
      </div>
    </details>
    """)


def get_chart_theme_config() -> dict:
    """Returns Plotly layout options and vibrant colorway based on active theme."""
    theme = get_current_theme()
    if theme == "light":
        return {
            "template": "plotly_white",
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font_color": "#0F172A",
            "gridcolor": "#E2E8F0",
            "zerolinecolor": "#CBD5E1",
            "primary_line": "#4F46E5",
            "primary_fill": "rgba(79, 70, 229, 0.16)",
            "palette": ["#4F46E5", "#06B6D4", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899"],
            "continuous_blues": [[0, "#EFF6FF"], [0.5, "#3B82F6"], [1, "#1D4ED8"]],
            "continuous_purples": [[0, "#FAF5FF"], [0.5, "#8B5CF6"], [1, "#5B21B6"]],
            "severity_map": {
                "LOW": "#10B981",
                "MEDIUM": "#F59E0B",
                "HIGH": "#EA580C",
                "CRITICAL": "#DC2626",
            },
        }
    else:
        return {
            "template": "plotly_dark",
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font_color": "#F8FAFC",
            "gridcolor": "rgba(51, 65, 85, 0.6)",
            "zerolinecolor": "rgba(71, 85, 105, 0.8)",
            "primary_line": "#00F2FE",
            "primary_fill": "rgba(0, 242, 254, 0.20)",
            "palette": ["#00F2FE", "#A855F7", "#10E7A0", "#FBBF24", "#FF3366", "#38BDF8", "#F472B6"],
            "continuous_blues": [[0, "#082f49"], [0.5, "#0284c7"], [1, "#00F2FE"]],
            "continuous_purples": [[0, "#2e1065"], [0.5, "#7c3aed"], [1, "#c084fc"]],
            "severity_map": {
                "LOW": "#10E7A0",
                "MEDIUM": "#FBBF24",
                "HIGH": "#FB7185",
                "CRITICAL": "#FF3366",
            },
        }