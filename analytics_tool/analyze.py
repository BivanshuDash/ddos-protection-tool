import os
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt

LOG_FILE = os.path.join(os.path.dirname(__file__), '../logs/access.log')

# Threshold for flagging (tune this)
REQUEST_THRESHOLD = 30

def detect_ddos():
    ip_count = defaultdict(int)

    with open(LOG_FILE, "r") as f:
        for line in f:
            try:
                ip, path, timestamp = line.strip().split(" - ")
                ip_count[ip] += 1
            except ValueError:
                continue  # Skip bad lines

    print("\n--- Traffic Analysis Report ---")
    for ip, count in sorted(ip_count.items(), key=lambda x: x[1], reverse=True):
        flag = "🚨 DDoS Suspect" if count > REQUEST_THRESHOLD else ""
        print(f"{ip}: {count} requests {flag}")
    
    return ip_count

if __name__ == "__main__":
    ip_count = detect_ddos()

    if ip_count:
        ips = list(ip_count.keys())
        counts = list(ip_count.values())

        plt.figure(figsize=(10, 5))
        plt.bar(ips, counts, color='orange')
        plt.axhline(y=REQUEST_THRESHOLD, color='red', linestyle='--', label='DDoS Threshold')
        plt.xlabel("IP Addresses")
        plt.ylabel("Request Count")
        plt.title("IP Traffic Analysis")
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        plt.savefig("../logs/traffic_report.png")
        print("\n📊 Graph saved to logs/traffic_report.png")
