from flask import Flask, request
from datetime import datetime
import os

app = Flask(__name__)

# Ensure logs directory exists
LOG_FILE = os.path.join(os.path.dirname(__file__), '../logs/access.log')
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

@app.route("/")
@app.route("/login")
@app.route("/data")
def index():
    ip = request.remote_addr
    path = request.path
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(LOG_FILE, "a") as f:
        f.write(f"{ip} - {path} - {time}\n")

    return f"✅ Welcome to {path}. Your IP: {ip}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
