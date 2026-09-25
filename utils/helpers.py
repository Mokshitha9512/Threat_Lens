"""ThreatLens — shared helper functions."""

from datetime import datetime
from utils.constants import (
    RISK_LOW_MAX, RISK_MEDIUM_MAX, RISK_HIGH_MAX,
    SEV_LOW, SEV_MEDIUM, SEV_HIGH, SEV_CRITICAL,
)


def severity_from_risk(score: int) -> str:
    if score <= RISK_LOW_MAX:
        return SEV_LOW
    if score <= RISK_MEDIUM_MAX:
        return SEV_MEDIUM
    if score <= RISK_HIGH_MAX:
        return SEV_HIGH
    return SEV_CRITICAL


def clamp_score(score: int) -> int:
    return max(0, min(100, int(score)))


def now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds")


def format_ip(ip: str) -> str:
    return (ip or "").strip()