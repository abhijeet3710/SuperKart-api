import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load serialized model pipeline
MODEL_PATH = "superkart_model.joblib"
try:
    model = joblib.load(MODEL_PATH)
except Exception:
    model = joblib.load("backend_files/superkart_model.joblib")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "online", "message": "SuperKart Flask API is running"})

@app.route("/v1/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        
        # Handle single dictionary or list of dictionaries (batch)
        if isinstance(data, dict):
            input_df = pd.DataFrame([data])
            prediction = model.predict(input_df)[0]
            return jsonify({"status": "success", "predicted_sales": float(prediction)})
        
        elif isinstance(data, list):
            input_df = pd.DataFrame(data)
            predictions = model.predict(input_df).tolist()
            return jsonify({"status": "success", "predicted_sales": predictions})
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
