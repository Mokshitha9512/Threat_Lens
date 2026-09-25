"""
ThreatLens — Risk scoring + severity mapping.
"""

from utils.constants import (
    CORRELATION_BONUS, CORRELATION_MIN_THREATS,
    SEV_LOW, SEV_MEDIUM, SEV_HIGH, SEV_CRITICAL,
    RISK_LOW_MAX, RISK_MEDIUM_MAX, RISK_HIGH_MAX,
)


def severity_from_score(score: int) -> str:
    if score <= RISK_LOW_MAX:
        return SEV_LOW
    if score <= RISK_MEDIUM_MAX:
        return SEV_MEDIUM
    if score <= RISK_HIGH_MAX:
        return SEV_HIGH
    return SEV_CRITICAL


def compute_incident_risk(alerts: list[dict]) -> dict:
    """
    Given a list of alert dicts (each with 'risk_score'), return:
    {
      "base_score": int,
      "correlation_bonus": int,
      "final_score": int,
      "severity": str,
      "unique_threat_types": int,
    }
    """
    base = sum(int(a.get("risk_score", 0)) for a in alerts)
    unique_types = len({a["threat_type"] for a in alerts})

    bonus = CORRELATION_BONUS if unique_types >= CORRELATION_MIN_THREATS else 0
    final = min(base + bonus, 100)

    return {
        "base_score": min(base, 100),
        "correlation_bonus": bonus,
        "final_score": final,
        "severity": severity_from_score(final),
        "unique_threat_types": unique_types,
    }