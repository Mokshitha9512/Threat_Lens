"""
ThreatLens — Incident Correlation Engine.
Groups related alerts from the same source into a single incident.
"""

from datetime import timedelta
from collections import defaultdict
from src.risk.risk_scoring import compute_incident_risk
from utils.constants import CORRELATION_WINDOW_MIN


def _build_title(threat_types: set[str]) -> str:
    """Generate human-readable incident title."""
    n = len(threat_types)
    if n == 1:
        return f"Potential {list(threat_types)[0].replace('_', ' ').title()}"
    if n == 2:
        parts = sorted(t.replace('_', ' ').title() for t in threat_types)
        return f"Suspicious {' + '.join(parts)} Activity"
    return "Potential Coordinated Intrusion"


def _build_description(source_ip: str, first, last, types: set[str], score: int) -> str:
    duration = int((last - first).total_seconds())
    type_list = ", ".join(sorted(t.replace('_', ' ').title() for t in types))
    return (
        f"Source {source_ip} triggered {len(types)} distinct threat behaviours "
        f"({type_list}) within a {duration}-second window. "
        f"Combined risk score: {score}/100."
    )


def correlate_alerts(alert_dicts: list[dict]) -> list[dict]:
    """
    Group alerts by source_ip + time window.
    Any group with >= 2 distinct threat types becomes an incident.
    """
    if not alert_dicts:
        return []

    # Parse timestamps
    parsed = []
    for a in alert_dicts:
        a = dict(a)
        a["_ts"] = _parse_ts(a["timestamp"])
        parsed.append(a)

    parsed.sort(key=lambda x: x["_ts"])

    window = timedelta(minutes=CORRELATION_WINDOW_MIN)
    incidents: list[dict] = []
    used = [False] * len(parsed)

    for i, anchor in enumerate(parsed):
        if used[i]:
            continue

        group = [anchor]
        used[i] = True

        for j in range(i + 1, len(parsed)):
            if used[j]:
                continue
            candidate = parsed[j]
            if candidate["source_ip"] != anchor["source_ip"]:
                continue
            if candidate["_ts"] - anchor["_ts"] > window:
                break
            group.append(candidate)
            used[j] = True

        types = {a["threat_type"] for a in group}
        if len(types) < 2:
            # Single-type groups are NOT incidents; they remain as standalone alerts
            continue

        risk = compute_incident_risk(group)
        first = min(a["_ts"] for a in group)
        last = max(a["_ts"] for a in group)

        incidents.append({
            "source_ip": anchor["source_ip"],
            "first_seen": first.isoformat(timespec="seconds"),
            "last_seen": last.isoformat(timespec="seconds"),
            "title": _build_title(types),
            "description": _build_description(
                anchor["source_ip"], first, last, types, risk["final_score"]
            ),
            "severity": risk["severity"],
            "risk_score": risk["final_score"],
            "base_score": risk["base_score"],
            "correlation_bonus": risk["correlation_bonus"],
            "threat_types": sorted(types),
            "alert_count": len(group),
            "alerts": group,
        })

    return incidents


def _parse_ts(ts):
    """Accept either datetime or ISO string."""
    from datetime import datetime
    if isinstance(ts, datetime):
        return ts
    return datetime.fromisoformat(ts)