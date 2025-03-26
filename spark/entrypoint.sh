#!/bin/bash
# Chờ Kafka và MinIO sẵn sàng
while ! nc -z kafka 9092; do sleep 1; done
while ! curl -s http://minio:9000/minio/health/ready; do sleep 1; done

# Submit Spark job
spark-submit \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 \
    /app/kafka_to_minio.py