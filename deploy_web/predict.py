import pickle
from flask import Flask, request, jsonify

with open('log_reg.bin', 'rb') as model:
    (dv, lr) = pickle.load(model)

def predict(features):
    # transform [{'feature1':int, 'feature2':int}, {'feature1':int, 'feature2':int}] into matrix
    features = dv.transform(features)

    pred = lr.predict(features)

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

