from flask import Flask, request, jsonify
import requests
from datetime import datetime
from pytz import timezone


app = Flask(__name__)

TARGET_URL = "https://buoy-img-report-default-rtdb.asia-southeast1.firebasedatabase.app/.json?auth=d6zIj1Mx25srICB2jgEgjdk1zm5IEe5qrcdZKhRu"

@app.route("/")
def home():
    return jsonify({"status": "Buoy Image report API is running"}), 200

@app.route('/relay', methods=['POST'])
def relay():
    data = request.get_json() or request.form.to_dict()
    ph_tz = timezone('Asia/Manila')
    data['timestamp'] = datetime.now(ph_tz).strftime("%m/%d/%Y %H:%M:%S")

    resp = requests.post(TARGET_URL, json=data)

    # Try to parse Firebase response
    try:
        resp_json = resp.json()
        name_value = resp_json.get("name", "")
    except Exception:
        name_value = resp.text  # fallback in case response isn't JSON

    return jsonify({
        "status": "forwarded",
        "id": name_value,        
        "target_status": resp.status_code
    })

if __name__ == '__main__':
    app.run()
