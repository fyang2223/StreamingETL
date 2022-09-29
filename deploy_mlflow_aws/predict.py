import mlflow
from flask import Flask, request, jsonify


TRACKING_SERVER = "http://localhost:5000"
RUN_ID = "7230d0e2c52d48b8bbf9d1d4b1525e9e"
MODEL_URI = f"s3://mlflow-forest/1/{RUN_ID}/artifacts/models"

# mlflow.set_tracking_uri(TRACKING_SERVER)
model = mlflow.pyfunc.load_model(model_uri=MODEL_URI)

def predict(features):
    pred = model.predict(features)
    return pred[0]


app = Flask('duration-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    features = request.get_json()
    pred = predict(features)

    result = {
        'duration': int(pred)
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)

