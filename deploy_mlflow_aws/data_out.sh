KINESIS_STREAM_OUTPUT='passenger_predictions'
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

echo ${RESULT} | jq -r '.Records[0].Data'