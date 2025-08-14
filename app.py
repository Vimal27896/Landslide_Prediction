from flask import Flask, request, jsonify
import pickle
import numpy as np
import os

# 1️⃣ Initialize Flask App
app = Flask(__name__)

# 2️⃣ Load the Model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'res.pkl')  # Better path handling

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Failed to load model: {str(e)}")
    model = None

# 3️⃣ Health Check Endpoint
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "ready" if model else "error",
        "message": "Landslide Prediction API",
        "model_loaded": bool(model)
    })

# 4️⃣ Prediction Endpoint (POST)
@app.route('/predict', methods=['POST'])
def predict_post():
    if not model:
        return jsonify({"error": "Model not loaded"}), 503
    
    try:
        data = request.json
        
        # Validate input
        if not data or 'features' not in data:
            return jsonify({"error": "Please provide 'features' in JSON body"}), 400
            
        features = data['features']
        
        if not isinstance(features, list) or len(features) == 0:
            return jsonify({"error": "'features' must be a non-empty list"}), 400

        # Convert and predict
        input_array = np.array(features, dtype=float).reshape(1, -1)
        prediction = model.predict(input_array)
        
        return jsonify({
            "prediction": float(prediction[0]),
            "status": "success",
            "input_features": features
        })

    except ValueError as e:
        return jsonify({"error": f"Invalid feature values: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

# 5️⃣ Prediction Endpoint (GET)
@app.route('/predict', methods=['GET'])
def predict_get():
    if not model:
        return jsonify({"error": "Model not loaded"}), 503
    
    try:
        features = request.args.getlist('features')
        
        if len(features) == 0:
            return jsonify({
                "error": "Please provide features as query parameters",
                "example": "/predict?features=0.1&features=0.2&features=0.3"
            }), 400

        # Convert and predict
        input_array = np.array([float(f) for f in features]).reshape(1, -1)
        prediction = model.predict(input_array)
        
        return jsonify({
            "prediction": float(prediction[0]),
            "status": "success",
            "input_features": features
        })

    except ValueError as e:
        return jsonify({"error": f"All features must be numbers: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

# 6️⃣ Run Flask Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)