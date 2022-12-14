import os
import requests
import lambda_function_ui_nomodel

os.environ["AWS_PROFILE"] = 'iamadmin'
os.environ["AWS_DEFAULT_REGION"] = 'us-east-1'

event = {
    'Records': [
        {
            'kinesis': {
                'kinesisSchemaVersion': '1.0', 
                'partitionKey': '1', 
                'sequenceNumber': '49633930873543048396023173467440720160140773540570857474', 
                'data': 'ewogICAgICAgICJmZWF0dXJlcyI6IHsKICAgICAgICAgICAgInQxIjogMiwKICAgICAgICAgICAgInQyIjogMywKICAgICAgICAgICAgImh1bSI6IDUwLAogICAgICAgICAgICAid2VhdGhlcl9jb2RlIjogMgogICAgICAgIH0sIAogICAgICAgICJwcmVkX2lkIjogMTIzCiAgICB9', 
                'approximateArrivalTimestamp': 1665202866.428
            }, 
            'eventSource': 'aws:kinesis', 
            'eventVersion': '1.0', 
            'eventID': 'shardId-000000000000:49633930873543048396023173467440720160140773540570857474', 
            'eventName': 'aws:kinesis:record', 
            'invokeIdentityArn': 'arn:aws:iam::082206757367:role/lambda-kinesis', 
            'awsRegion': 'us-east-1', 
            'eventSourceARN': 'arn:aws:kinesis:us-east-1:082206757367:stream/passenger_events'
        }
    ]
}

res = lambda_function_ui_nomodel.lambda_handler(event, None)
print(res)
