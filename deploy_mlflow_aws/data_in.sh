KINESIS_STREAM_INPUT=passenger_events

aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
    --data '{
        "features": {
            "Age": 130,
            "Pclass": 205,
            "Fare": 3.66
        }, 
        "pred_id": 123
    }' \
    --cli-binary-format raw-in-base64-out \
    --profile iamadmin




