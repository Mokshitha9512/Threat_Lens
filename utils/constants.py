"""
ThreatLens — Global Constants
Frozen in Phase 0. Do not modify without updating detection + risk modules.
"""

# ---------------- Risk Score Thresholds ----------------
RISK_LOW_MAX      = 29
RISK_MEDIUM_MAX   = 59
RISK_HIGH_MAX     = 79
RISK_CRITICAL_MAX = 100

# ---------------- Rule Score Contributions (LOCKED) ----------------
SCORE_PORT_SCAN        = 22
SCORE_BRUTE_FORCE      = 18
SCORE_TRAFFIC_FLOOD    = 18
SCORE_TRAFFIC_ANOMALY  = 12
SCORE_PROTOCOL_ANOMALY = 10
SCORE_ML_ANOMALY       = 15

# ---------------- Correlation ----------------
CORRELATION_BONUS       = 10
CORRELATION_WINDOW_MIN  = 10
CORRELATION_MIN_THREATS = 3

# ---------------- Detection Window Sizes ----------------
PORT_SCAN_WINDOW_SEC        = 60
PORT_SCAN_MIN_UNIQUE_PORTS  = 10
PORT_SCAN_MIN_EVENTS        = 10

BRUTE_FORCE_WINDOW_SEC      = 300
BRUTE_FORCE_MIN_FAILURES    = 10

TRAFFIC_FLOOD_MULTIPLIER    = 4.0
TRAFFIC_ANOMALY_MULTIPLIER  = 6.0

# ---------------- Threat Types ----------------
THREAT_PORT_SCAN        = "PORT_SCAN"
THREAT_BRUTE_FORCE      = "BRUTE_FORCE"
THREAT_TRAFFIC_FLOOD    = "TRAFFIC_FLOOD"
THREAT_TRAFFIC_ANOMALY  = "TRAFFIC_ANOMALY"
THREAT_PROTOCOL_ANOMALY = "PROTOCOL_ANOMALY"
THREAT_ML_ANOMALY       = "ML_ANOMALY"

# ---------------- Severity ----------------
SEV_LOW      = "LOW"
SEV_MEDIUM   = "MEDIUM"
SEV_HIGH     = "HIGH"
SEV_CRITICAL = "CRITICAL"

# ---------------- Status ----------------
STATUS_SUCCESS = "SUCCESS"
STATUS_FAILED  = "FAILED"
STATUS_DENIED  = "DENIED"