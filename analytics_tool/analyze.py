from collections import defaultdict
import matplotlib.pyplot as plt

log_file = "../logs/access.log"
threshold = 75 #Mark IPs with >20 requests as risky

ip_counts = defaultdict(int)

# Read logs and count requests per IP
with open(log_file, "r") as f:
    for line in f:
        if "-" in line:
            ip = line.split("-")[0].strip()
            ip_counts[ip] += 1

# Calculate risk scores (requests count for now)
risky_ips = {}
for ip, count in ip_counts.items():
    score = count
    if score > threshold:
        risky_ips[ip] = score

print("\n📊 IP Risk Analysis:")
print("-" * 30)
for ip, count in ip_counts.items():
    score = count
    flag = "⚠️ HIGH RISK" if ip in risky_ips else ""
    print(f"{ip:20} | Requests: {count:3} | Score: {score:3} {flag}")
print("-" * 30)
print(f"Total IPs scanned: {len(ip_counts)}")
print(f"High Risk IPs: {len(risky_ips)}")

def get_threat_level(risky_ips_count):
    if risky_ips_count == 0:
        return "Normal", "green"
    elif 1 <= risky_ips_count <= 5:
        return "Elevated", "yellow"
    else:
        return "Under Attack", "red"

threat_level, color = get_threat_level(len(risky_ips))

# Save the threat level to a text file for Flask to read
with open("threat_status.txt", "w") as f:
    f.write(f"{threat_level},{color}")

print(f"Threat Level: {threat_level}")

# Save risky IPs to file
with open("risky_ips.txt", "w") as f:
    for ip in risky_ips:
        f.write(ip + "\n")

# Split into normal and risky counts
normal_ips = {ip: count for ip, count in ip_counts.items() if ip not in risky_ips}
risky_ips_only = {ip: count for ip, count in ip_counts.items() if ip in risky_ips}

# Plotting
plt.figure(figsize=(10, 5))
plt.bar(normal_ips.keys(), normal_ips.values(), label="Normal IPs", color="green")
plt.bar(risky_ips_only.keys(), risky_ips_only.values(), label="Suspicious IPs", color="red")
plt.xticks(rotation=45, ha='right')
plt.xlabel("IP Address")
plt.ylabel("Request Count")
plt.title("Normal vs DDoS IPs")
plt.legend()
plt.tight_layout()
plt.savefig("../plots/ip_risk_comparison.png")
plt.close()

print("📉 Risk graph saved to plots/ip_risk_comparison.png")
