import pickle
from flask import Flask, request, jsonify

with open('pipe.bin', 'rb') as model:
    (dv,ct,lr) = pickle.load(model)

def prepare_features(features):
    features['t1t2'] = features['t1'] * features['t2']
    return features

def predict(features):
    features = dv.transform(features)
    features = ct.transform(features)
    pred = lr.predict(features)
    return pred[0]


app = Flask('duration-prediction')

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    features = request.get_json()
    features = prepare_features(features)
    pred = predict(features)

    result = {
        'cnt': int(pred)
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)

