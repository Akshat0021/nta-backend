from flask import Flask, jsonify
from flask_cors import CORS
import urllib.request
import os

app = Flask(__name__)
CORS(app)  # 👈 Allow all cross-origin requests

@app.route('/')
def home():
    return "NTA Tracker Backend Running"

@app.route('/run')
def run_tracker():
    logs = []
    for j in range(1000):
        logs.append(str(j))
        for i in range(100):
            if i < 10:
                url = f"https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2025/04/202504170{i}.pdf"
            else:
                url = f"https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2025/04/20250417{i}.pdf"
            try:
                response = urllib.request.urlopen(url)
                code = response.getcode()
                logs.append(f"{code} - {url}")
                return jsonify({"logs": logs, "success": True, "url": url})
            except:
                continue
    return jsonify({"logs": logs, "success": False})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
