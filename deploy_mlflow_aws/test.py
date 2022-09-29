import os
import requests

os.environ["AWS_PROFILE"] = 'iamadmin'

data = {
    "Records":[
        {
            "kinesis":{
                "kinesisSchemaVersion":"1.0",
                "partitionKey":"1",
                "sequenceNumber":"49633654682203477864432177173401237048670619738189070338",
                "data":"ewogICAgICAgICJmZWF0dXJlcyI6IHsKICAgICAgICAgICAgIkFnZSI6IDEzMCwKICAgICAgICAgICAgIlBjbGFzcyI6IDIwNSwKICAgICAgICAgICAgIkZhcmUiOiAzLjY2CiAgICAgICAgfSwgCiAgICAgICAgInByZWRfaWQiOiAxMjMKICAgIH0=",
                "approximateArrivalTimestamp":1664243692.468
            },
            "eventSource":"aws:kinesis",
            "eventVersion":"1.0",
            "eventID":"shardId-000000000000:49633654682203477864432177173401237048670619738189070338",
            "eventName":"aws:kinesis:record",
            "invokeIdentityArn":"arn:aws:iam::082206757367:role/lambda-kinesis",
            "awsRegion":"us-east-1",
            "eventSourceARN":"arn:aws:kinesis:us-east-1:082206757367:stream/passenger_events"
        }
    ]
}

# data = [{'Age':29, 'Pclass':1, 'Fare':20},
#         {'Age':29, 'Pclass':3, 'Fare':4}]
# data = {"Age":29, "Pclass":3, "Fare":4}

url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

response = requests.post(url, json=data)

print(response.json())





