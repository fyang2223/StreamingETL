import json
import base64
import boto3

CLIENT = boto3.client('kinesis')
OUTPUT_STREAM = 'bike-predictions'

def prepare_features(features):
    features['t1t2'] = features['t1'] * features['t2']
    return features

def predict(features):

    return 1

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
            "model": "test",
            "version": "gege",
            "prediction": {
                "cnt": prediction,
                "pred_id": pred_id
            }
        }
        
        CLIENT.put_record(
            StreamName=OUTPUT_STREAM,
            Data=json.dumps(pred_event), # Converts python object to a JSON string
            PartitionKey=str(pred_id)
        )
        
        predictions.append(pred_event)

    return {
        'predictions': predictions
    }
