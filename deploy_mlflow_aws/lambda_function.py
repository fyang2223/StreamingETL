import json
import base64
import boto3
import mlflow
import os

# os.environ['AWS_DEFAULT_REGION'] = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

CLIENT = boto3.client('kinesis')
RUN_ID = os.getenv('RUN_ID', '4302f22a1a7b4ce9a25a99b04bca2f0f')
OUTPUT_STREAM = os.getenv('OUTPUT_STREAM', 'bike-prediction-output-stream')
MODEL_URI = f"s3://mlflow-forest/2/{RUN_ID}/artifacts/models"

model = mlflow.pyfunc.load_model(model_uri=MODEL_URI)

def prepare_features(features):
    features['t1t2'] = features['t1'] * features['t2']
    return features

def predict(features):
    pred = model.predict(features)
    return int(pred[0])

def lambda_handler(event, context):
    predictions = [] # A list of pred_event objects

    for record in event.get('Records'):
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode("utf-8")
        dict_data = json.loads(decoded_data) # This takes a JSON string and converts it into a Python Dictionary.
        
        features = dict_data['features']
        features = prepare_features(features)
        
        pred_id = dict_data['pred_id']
        
        prediction = predict(features)
        pred_event = {
            'model': 'test',
            'version': 'one',
            "prediction": {
                'cnt': prediction,
                'pred_id': pred_id
            }
        }
        
        CLIENT.put_record(
            StreamName=OUTPUT_STREAM,
            Data=json.dumps(pred_event), # Converts python object to a JSON string
            PartitionKey=str(pred_id)
        )
        
        predictions.append(pred_event)

        print(json.dumps(pred_event))

    return {
        'predictions': predictions
    }
