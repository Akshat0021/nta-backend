from flask import Flask, jsonify
from flask_cors import CORS
import threading
import urllib.request
import time
import os

app = Flask(__name__)
CORS(app)

logs = []
found_url = None
status = "Running"
current_i = 0

def tracker_loop():
    global logs, found_url, status, current_i
    while found_url is None:
        for j in range(1000):
            logs.append(f"J loop: {j}")
            for i in range(0,100):
                if i == 49:
                    continue
                current_i = i
                logs.append(f"⏳ Running tracker... (i = {i})")
                if i < 10:
                    url = f"https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2025/04/202504170{i}.pdf"
                else:
                    url = f"https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2025/04/20250417{i}.pdf"
                try:
                    response = urllib.request.urlopen(url)
                    code = response.getcode()
                    logs.append(f"{code} - {url}")
                    found_url = url
                    status = "FOUND"
                    return
                except:
                    continue
            time.sleep(1)

@app.route("/logs")
def get_logs():
    return jsonify({
        "logs": logs[-100:],  # send last 100 log lines
        "status": status,
        "current_i": current_i,
        "url": found_url
    })

@app.route("/")
def home():
    return "NTA Tracker Backend Running"

if __name__ == "__main__":
    threading.Thread(target=tracker_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
