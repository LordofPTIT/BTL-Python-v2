from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MongoDB Atlas connection URI
# Replace <db_password> with your actual password
uri = "mongodb+srv://lcthinh286:<db_password>@cluster0.upmr8jn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Select the database and collections
db = client["phishing_db"]
reports_collection = db["reports"]
models_collection = db["models"]

# Define the Report model
class Report:
    def __init__(self, url, reason, timestamp=None):
        self.url = url
        self.reason = reason
        self.timestamp = timestamp if timestamp else datetime.utcnow()

    def to_dict(self):
        return {
            "url": self.url,
            "reason": self.reason,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["url"], data["reason"], data.get("timestamp"))

# Endpoint to get the model from MongoDB
@app.route('/model', methods=['GET'])
def get_model():
    model_doc = models_collection.find_one({"_id": "current_model"})
    if model_doc:
        return jsonify(model_doc["data"])
    else:
        return jsonify({"error": "Model not found"}), 404

# Endpoint to report a site
@app.route('/report', methods=['POST'])
def report_site():
    data = request.json
    report = Report(url=data['url'], reason=data['reason'])
    reports_collection.insert_one(report.to_dict())
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)