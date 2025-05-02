from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import pymongo
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Kết nối MongoDB
client = pymongo.MongoClient("mongodb+srv://lcthinh286:Kaidotuhoang1@@cluster0.upmr8jn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["phishing_db"]
reports_collection = db["reports"]

@app.route('/model', methods=['GET'])
def get_model():
    return send_from_directory('.', 'model.json')

@app.route('/report', methods=['POST'])
def report_site():
    data = request.json
    report = {
        'url': data['url'],
        'reason': data['reason'],
        'timestamp': datetime.utcnow()
    }
    reports_collection.insert_one(report)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)