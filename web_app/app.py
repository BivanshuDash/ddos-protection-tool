from flask import Flask, request, render_template_string, redirect, url_for
import time
import random
import subprocess
import datetime
import string

app = Flask(__name__)
log_file = "../logs/access.log"

# Function to generate unique IPs
def generate_unique_ip(prefix="192.168"):
    # Create random IP by appending a random number to the prefix
    unique_id = ''.join(random.choices(string.digits, k=3))  # Generates a 3-digit number
    return f"{prefix}.{unique_id}"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>DDoS Protection Tool</title>
    <style>
        body { font-family: sans-serif; text-align: center; margin-top: 50px; }
        button { padding: 10px 20px; font-size: 18px; margin: 20px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>🛡️ Welcome to DDoS Defense Demo</h1>
    <form method="POST" action="/simulate">
        <button type="submit">💣 Simulate DDoS Attack</button>
    </form>
    <p><a href="/view-log">🔍 View Access Log</a></p>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_TEMPLATE)

def simulate_request(ip, path="/"):
    log_entry = f'{ip} - - [{datetime.datetime.now().strftime("%d/%b/%Y:%H:%M:%S")}] "GET {path} HTTP/1.1" 200 1234\n'
    with open(log_file, "a") as f:
        f.write(log_entry)

@app.route("/simulate", methods=["POST"])
def simulate_ddos():
    target = request.form.get("target", "/")
    normal_count = int(request.form.get("normal", 10))
    attacker_count = int(request.form.get("attack", 1))
    attack_intensity = int(request.form.get("intensity", 100))

    # Normal users (many unique IPs, low volume)
    for i in range(normal_count):
        ip = generate_unique_ip()  # Create a unique IP each time
        for _ in range(random.randint(3, 8)):  # Normal traffic (3-8 requests)
            simulate_request(ip, target)

    # Attackers (few unique IPs, high volume)
    for i in range(attacker_count):
        ip = generate_unique_ip(prefix="10.0")  # Use a different prefix for attackers
        for _ in range(attack_intensity):  # High traffic intensity
            simulate_request(ip, target)

    return redirect("/")

@app.route("/view-log", methods=["GET"])
def view_log():
    with open(log_file, "r") as f:
        log_data = f.readlines()
    return "<pre>" + "".join(log_data[-20:]) + "</pre>"  # last 20 lines

if __name__ == "__main__":
    app.run(port=5001, debug=True)
