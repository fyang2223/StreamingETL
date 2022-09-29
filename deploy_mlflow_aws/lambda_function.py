import json
import base64
import boto3
import mlflow
import os

CLIENT = boto3.client('kinesis')
OUTPUT_STREAM = os.environ['OUTPUT_STREAM']
RUN_ID = os.environ['RUN_ID']
MODEL_URI = f"s3://mlflow-forest/1/{RUN_ID}/artifacts/models"

def predict(features):

    model = mlflow.pyfunc.load_model(model_uri=MODEL_URI)    
    pred = model.predict(features)[0]

    return int(pred)

def lambda_handler(event, context):
    predictions = []
    
    for record in event.get('Records'):
        encoded_data = record.get('kinesis',{}).get('data')
        decoded_data = base64.b64decode(encoded_data).decode("utf-8")
        json_data = json.loads(decoded_data)

        features = json_data['features']
        prediction_id = json_data['pred_id']
        
        prediction = predict(features)
        pred_event = {
            "model": "test",
            "version": "gege",
            "prediction": {
                "survived": prediction,
                "pred_id": prediction_id
            }
        }
        
        CLIENT.put_record(
            StreamName=OUTPUT_STREAM,
            Data=json.dumps(pred_event),
            PartitionKey=str(prediction_id)
        )
        
        
        predictions.append(pred_event)

    return {
        'predictions': predictions
    }
