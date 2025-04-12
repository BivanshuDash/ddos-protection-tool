import os
import platform
from collections import defaultdict

LOG_FILE = os.path.join(os.path.dirname(__file__), '../logs/access.log')
BLOCK_THRESHOLD = 75  # Match analyzer threshold
BLOCKED_IPS_LOG = os.path.join(os.path.dirname(__file__), 'blocked_ips.txt')

def get_suspicious_ips():
    ip_count = defaultdict(int)
    with open(LOG_FILE, "r") as f:
        for line in f:
            if "-" in line:
                ip = line.split("-")[0].strip()
                ip_count[ip] += 1
    return [ip for ip, count in ip_count.items() if count > BLOCK_THRESHOLD]

def block_ip(ip):
    system = platform.system()
    if system == "Linux":
        print(f"🛡️ Blocking IP via iptables: {ip}")
        os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
    else:
        print(f"🧪 [MOCK BLOCK] Would block IP: {ip}")
        with open(BLOCKED_IPS_LOG, "a") as f:
            f.write(f"{ip}\n")

def main():
    print("🔍 Scanning for suspicious IPs...")
    suspicious_ips = get_suspicious_ips()

    if not suspicious_ips:
        print("✅ No DDoS detected. All good!")
        return

    for ip in suspicious_ips:
        block_ip(ip)

    print("✅ Auto-defense process completed.")

if __name__ == "__main__":
    main()
