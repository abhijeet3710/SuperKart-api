import os
import io
import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Resolve model path flexibly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "superkart_model.joblib")

if not os.path.exists(MODEL_PATH):
    MODEL_PATH = "superkart_model.joblib"

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "online", "message": "SuperKart Flask API is running"})

# Single JSON Prediction Endpoint
@app.route("/v1/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"status": "error", "message": "Model not loaded"}), 500

    try:
        data = request.get_json(force=True)
        if isinstance(data, dict):
            input_df = pd.DataFrame([data])
        elif isinstance(data, list):
            input_df = pd.DataFrame(data)
        else:
            return jsonify({"status": "error", "message": "Invalid payload format"}), 400

        predictions = model.predict(input_df).tolist()
        return jsonify({
            "status": "success",
            "predicted_sales": predictions if len(predictions) > 1 else predictions[0]
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# Batch File Upload Prediction Endpoint (CSV)
@app.route("/v1/predict_batch", methods=["POST"])
def predict_batch():
    if model is None:
        return jsonify({"status": "error", "message": "Model not loaded"}), 500

    try:
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file uploaded under key 'file'"}), 400

        file = request.files['file']
        content = file.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(content))

        predictions = model.predict(df).tolist()
        return jsonify({"status": "success", "predicted_sales": predictions})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
