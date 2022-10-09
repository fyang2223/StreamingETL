# The Lambda Function
The Lambda function's `event` variable is the same as what is passed to the `Event JSON` option in `Tests`.

# Architecture
The Lambda function is triggered by a Kinesis stream, which then outputs to another Kinesis stream.

# Run Instructions (Local/UI)
First copy the contents of `lambda_function_ui_nomodel.py` to a new Lambda function in the AWS UI. Attach the necessary permissions policies. In this Lambda function, a prediction is generated from the input features, and added to an event dictionary object, which is then pushed to a different output Kinesis stream. To inject a test featureset into the input Kinesis stream, execute:
```
./data_in.sh
```

To pull data from shards in the ouput stream, execute:
```
./data_out.sh
```
To test the function locally, use `python test.py` as it tests `lambda_function_ui_nomodel.py`.

# Run Instructions (Lambda Docker)
To serve the `lambda_function.py` script in Docker, first set the environment variable `TEST_RUN=False` in Docker if you want to put a record into the output Kinesis stream. 
```
docker build -t bike-prediction:v1 .

winpty docker run -it --rm \
    -p 8080:8080 \
    -e OUTPUT_STREAM="bike-predictions" \
    -e RUN_ID="4302f22a1a7b4ce9a25a99b04bca2f0f" \
    -e TEST_RUN="False" \
    -e AWS_DEFAULT_REGION="us-east-1" \
    -e AWS_ACCESS_KEY_ID="1234567890EXAMPLE" \
    -e AWS_SECRET_ACCESS_KEY="12345678901234567890EXAMPLE" \
    bike-prediction:v1

pipenv run python test_docker.py
```

Then to publish the image to ECR (taken from ECR UI):
```
aws ecr get-login-password --region us-east-1 --profile iamadmin | docker login --username AWS --password-stdin 082206757367.dkr.ecr.us-east-1.amazonaws.com

docker tag bike-prediction:v1 082206757367.dkr.ecr.us-east-1.amazonaws.com/bike-model:v1

docker push 082206757367.dkr.ecr.us-east-1.amazonaws.com/bike-model:v1
```

# Run Instructions (Lambda Container Image)
Set Lambda memory to 256mb, and use the ECR image above. Set environment variables `OUTPUT_STREAM="bike-predictions"` and `RUN_ID="4302f22a1a7b4ce9a25a99b04bca2f0f"`. Attach the Kinesis trigger as before, and run with `./data_in.sh` followed by `./data_out.sh`.



# Explanation
We first put a record into the ingestion Kinesis stream with the following commands (execute with `./data_in.sh`). Note that the data is a JSON STRING, so that when it is decoded in the Lambda function, it is still a JSON STRING, not Python Dictionary, thus it needs to be translated into a python dict before access operations can be done on it. 
```
KINESIS_STREAM_INPUT=passenger_events

aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
    --data '{
        "features": {
            "t1": 2,
            "t2": 3,
            "hum": 50,
            "weather_code": 2
        }, 
        "pred_id": 123
    }' \
    --cli-binary-format raw-in-base64-out \
    --profile iamadmin
```

The Lambda function is then triggered and the following is what the `event` variable contains (note the data sent in the `--data` field above is encoded into base64, and that this is a python dict, not JSON): 
```
{
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
```

Alternatively, to test the Lambda function independently, copy the following into the `Event JSON` field in the `Test` tab. This is the equivalent of using the `aws kinesis put-record` command above. This JSON object is then turned into a python dictionary (as above), and then passed into the Lambda function's `event` variable. The result is the same as above.
```
{
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "123456789123456789123456789",
                "data": "ewogICAgICAgICJmZWF0dXJlcyI6IHsKICAgICAgICAgICAgInQxIjogMiwKICAgICAgICAgICAgInQyIjogMywKICAgICAgICAgICAgImh1bSI6IDUwLAogICAgICAgICAgICAid2VhdGhlcl9jb2RlIjogMgogICAgICAgIH0sIAogICAgICAgICJwcmVkX2lkIjogMTIzCiAgICB9",
                "approximateArrivalTimestamp": 1665200574.31
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:123456789012345678901234567890",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::123456789012:role/lambda-kinesis",
            "awsRegion": "us-east-1",
            "eventSourceARN": "arn:aws:kinesis:us-east-1:123456789012:stream/passenger_events"
        }
    ]
}
```

A shard iterator specifies the shard position from which to start reading data records sequentially. The position is specified using the sequence number of a data record in a shard. A sequence number is the identifier associated with every record ingested in the stream, and is assigned when a record is put into the stream. Each stream has one or more shards.


