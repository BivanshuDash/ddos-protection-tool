from flask import Flask, request, render_template_string, redirect, url_for
import time
import random

app = Flask(__name__)
log_file = "../logs/access.log"

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

@app.route("/simulate", methods=["POST"])
def simulate_ddos():
    attacker_ip = f"192.168.1.{random.randint(10, 200)}"
    for _ in range(60):  # burst of traffic
        with open(log_file, "a") as f:
            f.write(f"{attacker_ip} - /login - {time.time()}\n")
        time.sleep(0.05)
    return redirect(url_for("index"))

@app.route("/view-log", methods=["GET"])
def view_log():
    with open(log_file, "r") as f:
        log_data = f.readlines()
    return "<pre>" + "".join(log_data[-20:]) + "</pre>"  # last 20 lines

if __name__ == "__main__":
    app.run(port=5001, debug=True)
