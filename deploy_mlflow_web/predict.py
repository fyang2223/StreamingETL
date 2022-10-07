import mlflow
import os
from flask import Flask, request, jsonify

os.environ['AWS_PROFILE'] = 'iamadmin'

RUN_ID = "4302f22a1a7b4ce9a25a99b04bca2f0f"
MODEL_URI = f"s3://mlflow-forest/2/{RUN_ID}/artifacts/models"

model = mlflow.pyfunc.load_model(model_uri=MODEL_URI)

def prepare_features(features):
    features['t1t2'] = features['t1'] * features['t2']
    return features

def predict(features):
    pred = model.predict(features)
    return pred[0]


app = Flask('duration-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    features = request.get_json()
    features = prepare_features(features)
    pred = model.predict(features)

    result = {
        'cnt': int(pred)
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)


