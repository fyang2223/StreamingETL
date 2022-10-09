#!/bin/bash

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
        "pred_id": 999
    }' \
    --cli-binary-format raw-in-base64-out \
    --profile iamadmin

