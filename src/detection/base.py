"""ThreatLens — common contract for all detection modules."""

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Alert:
    """Canonical alert shape. Every detector must return these."""
    threat_type: str            # e.g. PORT_SCAN
    source_ip: str
    destination_ip: str
    timestamp: str              # ISO 8601
    severity: str               # LOW / MEDIUM / HIGH / CRITICAL
    risk_score: int             # contribution to incident score
    description: str
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["evidence_json"] = str(self.evidence)
        d.pop("evidence", None)
        return d