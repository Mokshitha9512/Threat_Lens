import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

mods = [
    "utils.constants",
    "utils.helpers",
    "utils.state",
    "utils.ui",
    "src.detection",
    "src.detection.port_scan",
    "src.anomaly.isolation_forest",
    "src.correlation.incident_engine",
    "src.risk.risk_scoring",
]

for m in mods:
    try:
        __import__(m)
        print(f"✅ {m}")
    except Exception as e:
        print(f"❌ {m}  →  {type(e).__name__}: {e}")