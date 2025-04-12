# 🚨 DDoS Protection Architecture for Cloud

## 🧠 Objective:
To build a cloud-based system that detects, analyzes, and auto-mitigates DDoS attacks.

---

## 🔧 Tools & Features:
- `web_app`: Simulates real traffic using a Flask server
- `analytics_tool`: Detects DDoS patterns using access logs
- `auto_defender`: Automatically blocks high-frequency attackers (via iptables)
- `cloud_infra`: AWS EC2 + Nginx + CloudWatch monitoring

---

## ☁️ Cloud Architecture:
![Cloud Architecture](cloud_infra/ddos_architecture.png)

---

## 🧪 How It Works:
1. Flask logs incoming traffic with IP + path
2. Analytics script scans logs and flags suspicious IPs
3. Defender script blocks IPs or simulates blocking
4. Visual graph generated to support review

---

## 📦 Project Structure:

ddos-protection-tool/
├── README.md                # Project overview and documentation
├── requirements.txt         # Python dependencies
├── analytics_tool/          # DDoS detection logic
│   └── analyze.py           # Script to analyze access logs
├── auto_defender/           # IP blocking mechanism
│   ├── blocked_ips.txt      # Log of blocked IPs
│   └── defender.py          # Script to block suspicious IPs
├── cloud_infra/             # Cloud infrastructure resources
├── logs/                    # Logs and reports
│   ├── access.log           # Traffic logs
│   └── traffic_report.png   # Visualization of traffic analysis
├── scripts/                 # Additional utility scripts (empty for now)
└── web_app/                 # Flask application for simulating traffic
    └── app.py               # Web server implementation


---

## ✅ Outcome:
A multi-layered DDoS defense simulation that’s production-scalable and ready for AWS deployment.
