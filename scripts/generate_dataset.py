"""ThreatLens — Synthetic network log generator (Windows-safe paths)."""

import random
from datetime import datetime, timedelta
from pathlib import Path
import csv

random.seed(42)

OUT_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_network_logs.csv"

NORMAL_IPS = [f"192.168.1.{i}" for i in range(10, 40)]
DEST_IPS   = [f"10.0.0.{i}" for i in range(1, 20)]
ATTACKER   = "192.168.1.50"
VICTIM     = "10.0.0.12"

NORMAL_PORTS = [80, 443, 53, 22, 8080, 3306]
NORMAL_PROTO = ["TCP", "UDP", "TCP", "TCP", "UDP"]


# Realistic protocol↔port pairing
PORT_PROTOCOL_MAP = {
    80:   "TCP",
    443:  "TCP",
    53:   "UDP",
    22:   "TCP",
    8080: "TCP",
    3306: "TCP",
}


def rand_normal_event(ts):
    dest_port = random.choice(list(PORT_PROTOCOL_MAP.keys()))
    proto = PORT_PROTOCOL_MAP[dest_port]
    return {
        "timestamp": ts.isoformat(timespec="seconds"),
        "source_ip": random.choice(NORMAL_IPS),
        "destination_ip": random.choice(DEST_IPS),
        "source_port": random.randint(1024, 65535),
        "destination_port": dest_port,
        "protocol": proto,
        "packet_count": random.randint(1, 30),
        "packet_size": random.randint(60, 1500),
        "bytes_transferred": random.randint(200, 50000),
        "connection_duration": round(random.uniform(0.1, 3.0), 2),
        "status": "SUCCESS" if random.random() > 0.05 else "FAILED",
        "failed_attempts": 0,
        "is_suspicious": 0,
    }


def build_dataset():
    rows = []
    base = datetime(2025, 1, 15, 10, 0, 0)

    # 25000 normal events
    for _ in range(25000):
        ts = base + timedelta(seconds=random.randint(0, 3600))
        rows.append(rand_normal_event(ts))

    # Attack 1: Port scan (2 attempts per port = 28 events total)
    scan_start = base + timedelta(minutes=31)
    scan_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 1433, 3306, 3389]
    for i, port in enumerate(scan_ports):
        for repeat in range(2):
            rows.append({
                "timestamp": (scan_start + timedelta(seconds=i * 2 + repeat * 0.5)).isoformat(timespec="seconds"),
                "source_ip": ATTACKER, "destination_ip": VICTIM,
                "source_port": random.randint(40000, 60000),
                "destination_port": port, "protocol": "TCP",
                "packet_count": 1, "packet_size": 60, "bytes_transferred": 60,
                "connection_duration": 0.05, "status": "DENIED",
                "failed_attempts": 0, "is_suspicious": 1,
            })

    # Attack 2: Brute force
    bf_start = base + timedelta(minutes=33)
    for i in range(25):
        rows.append({
            "timestamp": (bf_start + timedelta(seconds=i * 4)).isoformat(timespec="seconds"),
            "source_ip": ATTACKER, "destination_ip": VICTIM,
            "source_port": random.randint(40000, 60000),
            "destination_port": 22, "protocol": "TCP",
            "packet_count": 3, "packet_size": 120, "bytes_transferred": 360,
            "connection_duration": 0.3, "status": "FAILED",
            "failed_attempts": i + 1, "is_suspicious": 1,
        })

    # Attack 3: Traffic flood
    flood_start = base + timedelta(minutes=34)
    for i in range(300):
        rows.append({
            "timestamp": (flood_start + timedelta(seconds=i // 5)).isoformat(timespec="seconds"),
            "source_ip": ATTACKER, "destination_ip": VICTIM,
            "source_port": random.randint(40000, 60000),
            "destination_port": 80, "protocol": "TCP",
            "packet_count": random.randint(50, 200),
            "packet_size": random.randint(1200, 1500),
            "bytes_transferred": random.randint(80000, 300000),
            "connection_duration": 0.1, "status": "SUCCESS",
            "failed_attempts": 0, "is_suspicious": 1,
        })

    # Attack 4: Protocol anomaly
    proto_start = base + timedelta(minutes=35)
    for i in range(5):
        rows.append({
            "timestamp": (proto_start + timedelta(seconds=i * 5)).isoformat(timespec="seconds"),
            "source_ip": ATTACKER, "destination_ip": VICTIM,
            "source_port": random.randint(40000, 60000),
            "destination_port": 22, "protocol": "UDP",
            "packet_count": 1, "packet_size": 512, "bytes_transferred": 512,
            "connection_duration": 0.05, "status": "SUCCESS",
            "failed_attempts": 0, "is_suspicious": 1,
        })

    random.shuffle(rows)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"[ThreatLens] Wrote {len(rows)} events -> {OUT_PATH}")


if __name__ == "__main__":
    build_dataset()