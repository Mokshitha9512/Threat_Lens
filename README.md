# 🛡️ ThreatLens

**Network Security Analytics & Intrusion Investigation Platform**

> Turn scattered network events into understandable security incidents.

ThreatLens is a Python web application that analyzes network traffic logs, detects multiple classes of suspicious behaviour using both rule-based and machine-learning techniques, correlates related alerts into a single incident, and provides an interactive SOC-style dashboard for investigation.

Built for a 6-hour hackathon — defensive security analysis only, no real-world attack functionality.

---

## 🎯 What It Does

ThreatLens takes raw network logs and transforms them into **prioritized security incidents** through a multi-stage pipeline:

1. **Detect** — 5 rule-based detectors + 1 ML anomaly detector flag suspicious events
2. **Correlate** — Alerts from the same source IP within a time window are grouped
3. **Score** — A transparent 0–100 risk score is computed
4. **Investigate** — Analysts see the incident story, evidence, and timeline

---

## 🛡️ Detections

| Detection | Method | Score |
|---|---|---|
| **Port Scan** | Rule-based — ≥10 unique ports in 60s | +22 |
| **Brute Force** | Rule-based — ≥10 failed logins in 5 min | +18 |
| **Traffic Flood** | Statistical — events/min > baseline × 4 | +18 |
| **Traffic Anomaly** | Statistical — bytes > global median × 6 | +12 |
| **Protocol Anomaly** | Rule-based — unusual protocol ↔ port pairing | +10 |
| **ML Anomaly** | Isolation Forest — behavioural outlier | +15 |
| **Correlation Bonus** | 3+ distinct threat types from same IP in 10 min | +10 |

Risk score is capped at **100** and mapped to severity:

| Score | Severity |
|---|---|
| 0–29 | LOW |
| 30–59 | MEDIUM |
| 60–79 | HIGH |
| 80–100 | CRITICAL |

---

## 🧠 The Differentiator — Incident Correlation

Instead of showing isolated alerts, ThreatLens **correlates related alerts** from the same source IP into a single incident.

Example: an attacker triggers 5 different behaviours in a 5-minute window:

```
192.168.1.50
      │
      ├── Port Scan          [HIGH]      +22
      ├── Brute Force        [CRITICAL]  +18
      ├── Traffic Flood      [CRITICAL]  +18
      ├── Traffic Anomaly    [HIGH]      +12
      ├── Protocol Anomaly   [MEDIUM] ×5 +10
      └── ML Anomaly         [MEDIUM]    +15
                    │
                    ▼
          INCIDENT: Potential Coordinated Intrusion
          Risk: 100/100 · CRITICAL
```

**One incident, one story, full evidence trail.**

---

## 🖥️ Pages

| Page | Purpose |
|---|---|
| 🛡️ **Welcome** | Hero overview, detection coverage |
| 📊 **Dashboard** | SOC overview — metric cards, activity charts, recent incidents |
| 📥 **Analyze** | Run demo scenario, upload custom CSV |
| 🚨 **Incidents** | Correlated incidents with timeline and evidence |
| 📈 **Analytics** | Protocol distribution, top IPs, bytes over time |
| 🔎 **IP Investigation** | Deep-dive a single source IP |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11 or 3.12**
- **pip**
- Any modern browser

### 1. Clone the project

```bash
git clone https://github.com/Mokshitha9512/Threat_Lens.git
cd Threat_Lens
```

### 2. Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate the sample dataset

```bash
python scripts/generate_dataset.py
```

### 5. Run the app

```bash
python -m streamlit run app.py
```

Open **http://localhost:8501** in your browser.

### 6. Run the demo

1. Click **📥 Analyze** in the sidebar
2. Click **▶️ Run Demo Scenario**
3. Navigate to **📊 Dashboard** and **🚨 Incidents**

You should see **1 CRITICAL incident** from source IP `192.168.1.50`.

---

## 📁 Project Structure

```
Threat_Lens/
├── app.py                          # Entry point (welcome page)
├── requirements.txt
├── README.md
├── .gitignore
│
├── .streamlit/
│   └── config.toml                 # Dark SOC theme
│
├── data/
│   └── sample_network_logs.csv     # 25,358 simulated events
│
├── pages/
│   ├── 1_SOC_Operations.py
│   ├── 2_Intrusion_Scanner.py
│   ├── 3_Active_Incidents.py
│   ├── 4_Network_Telemetry.py
│   └── 5_Entity_Forensics.py
│
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── detection/
│   │   ├── base.py
│   │   ├── port_scan.py
│   │   ├── brute_force.py
│   │   ├── traffic_flood.py
│   │   ├── traffic_anomaly.py
│   │   └── protocol_anomaly.py
│   ├── anomaly/
│   │   └── isolation_forest.py
│   ├── correlation/
│   │   └── incident_engine.py
│   ├── risk/
│   │   └── risk_scoring.py
│   └── database/
│       └── database.py
│
├── utils/
│   ├── constants.py
│   ├── helpers.py
│   ├── state.py
│   └── ui.py
│
└── scripts/
    ├── generate_dataset.py
    ├── test_detection.py
    └── test_phase3.py
```

---

## 📊 Dataset Schema

The synthetic generator produces network events with these columns:

| Column | Type | Description |
|---|---|---|
| `timestamp` | datetime | Event time |
| `source_ip` | str | Origin IP |
| `destination_ip` | str | Target IP |
| `source_port` | int | Source port |
| `destination_port` | int | Target port |
| `protocol` | str | TCP / UDP / ICMP |
| `packet_count` | int | Packets in event |
| `packet_size` | int | Avg packet size (bytes) |
| `bytes_transferred` | int | Total bytes |
| `connection_duration` | float | Seconds |
| `status` | str | SUCCESS / FAILED / DENIED |
| `failed_attempts` | int | Cumulative failures |

**Injected attacks:**
- Port scan (14 ports × 2 attempts) at 10:31
- Brute force (25 failed logins) at 10:33
- Traffic flood (300 events) at 10:34
- Protocol anomaly (5 UDP-on-22 events) at 10:35

All from source `192.168.1.50` targeting `10.0.0.12`.

---

## 🧪 Testing

```bash
# Rule-based detection
python scripts/test_detection.py

# Full pipeline with ML + correlation
python scripts/test_phase3.py
```

Expected: all detectors trigger, 1 CRITICAL incident from `192.168.1.50`.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.12 |
| **Web Framework** | Streamlit |
| **Data** | pandas, NumPy |
| **ML** | scikit-learn (Isolation Forest) |
| **Visualization** | Plotly |
| **Storage** | SQLite |
| **Testing** | pytest |

---

## 🔒 Security Boundary

ThreatLens is a **defensive analysis tool only**. It:

- ✅ Analyzes **simulated** network logs
- ✅ Detects patterns in **static** data
- ✅ Runs **locally** with no network access

It does **NOT**:

- ❌ Perform real network scanning
- ❌ Send real traffic
- ❌ Collect credentials
- ❌ Exploit any system

---

## 🎬 Demo Script (90 seconds)

1. **Open Dashboard** → shows clean SOC with all metrics
2. **Go to Analyze** → click **Run Demo Scenario**
3. **System processes 25K events** → detection runs
4. **Return to Dashboard** → 1 CRITICAL incident appears
5. **Open Incidents** → see `Potential Coordinated Intrusion` for `192.168.1.50`
6. **Expand "Why Was This Flagged?"** → shows base score + correlation bonus
7. **View Attack Timeline** → 10:31 Port Scan → 10:35 Protocol Anomaly
8. **Open IP Investigation** → deep-dive `192.168.1.50`

**Closing line:**

> *"Instead of presenting hundreds of independent alerts, ThreatLens turns related network events into an understandable incident story."*

---

## 📄 License

MIT — free to use, modify, and learn from.

---

**ThreatLens** · Turn network events into understandable security incidents.
