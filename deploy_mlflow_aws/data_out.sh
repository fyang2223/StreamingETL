KINESIS_STREAM_OUTPUT='bike-prediction-output-stream'
SHARD='shardId-000000000000'

SHARD_ITERATOR=$(aws kinesis get-shard-iterator \
    --shard-id ${SHARD} \
    --shard-iterator-type TRIM_HORIZON \
    --stream-name ${KINESIS_STREAM_OUTPUT} \
    --query 'ShardIterator' \
    --profile iamadmin \
    --region us-east-1 \
)

RESULT=$(aws kinesis get-records \
    --shard-iterator $SHARD_ITERATOR \
    --profile iamadmin \
    --region us-east-1 \
    --output "json" \
)

echo ${RESULT} | jq

# echo ${RESULT} | jq -r '.Records[0].Data' | base64 -i --decode | jq

# {
#  "Records": [],
#  "NextShardIterator": "AAAAAAAAAAG5oVfbsLwhuMi7UCD6CZok6JlYPCRnuqfoaWUP+UI3UDVqhi6QUVRmDsG+QPCfXFXehG8Dmrh+lu4fOvrtHF/VbseLSr683GOtAIDGhrI+7gAAP2KBMVVSVVJXXOQnYMLLIYuUQ7yLxTuPE1gz+E6zxS5+/Y5g1JblbQ8O9tv7ypYzFjTDq9r30tl1VgyY9VJxk3CLz910T+YM1liWVIAT2rwOnsJtr7FSkIEjOYrxMEBvKTqolZCAHXOiJS7r/Ag=",
#  "MillisBehindLatest": 85836000
#  }
