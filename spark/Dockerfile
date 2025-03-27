FROM docker.io/bitnami/spark:3.5

USER root

COPY ./jars/*.jar /opt/bitnami/spark/jars

# Install prerequisites
# RUN apt-get update && apt-get install -y curl

# RUN curl -O https://repo1.maven.org/maven2/software/amazon/awssdk/s3/2.20.135/s3-2.20.135.jar \
#     && curl -O https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.12.51/aws-java-sdk-1.12.51.jar \
#     && curl -O https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.4.0/delta-core_2.12-2.4.0.jar \
#     && curl -O https://repo1.maven.org/maven2/io/delta/delta-storage/2.4.0/delta-storage-2.4.0.jar \
#     && curl -O https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.33/mysql-connector-java-8.0.33.jar \
#     && curl -O https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.0/spark-sql-kafka-0-10_2.12-3.5.0.jar \
#     && curl -O https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.5.0/kafka-clients-3.5.0.jar \
#     && curl -O https://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-10_2.12/3.5.0/spark-streaming-kafka-0-10_2.12-3.5.0.jar \
#     && curl -O https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.0/spark-token-provider-kafka-0-10_2.12-3.5.0.jar \
#     && mv s3-2.20.135.jar /opt/bitnami/spark/jars \
#     && mv aws-java-sdk-1.12.51.jar /opt/bitnami/spark/jars \
#     && mv delta-core_2.12-2.4.0.jar /opt/bitnami/spark/jars \
#     && mv delta-storage-2.4.0.jar /opt/bitnami/spark/jars \
#     && mv mysql-connector-java-8.0.33.jar /opt/bitnami/spark/jars \
#     && mv spark-sql-kafka-0-10_2.12-3.5.0.jar /opt/bitnami/spark/jars \
#     && mv kafka-clients-3.5.0.jar /opt/bitnami/spark/jars \
#     && mv spark-streaming-kafka-0-10_2.12-3.5.0.jar /opt/bitnami/spark/jars \
#     && mv spark-token-provider-kafka-0-10_2.12-3.5.0.jar /opt/bitnami/spark/jars

RUN export PYSPARK_SUBMIT_ARGS="--master spark://spark-master:7077 pyspark-shell"
# curl -O https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.5.0/kafka-clients-3.5.0.jar && mv kafka-clients-3.5.0.jar /opt/bitnami/spark/jars
# curl -O https://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-10_2.12/3.5.0/spark-streaming-kafka-0-10_2.12-3.5.0.jar && mv spark-streaming-kafka-0-10_2.12-3.5.0.jar /opt/bitnami/spark/jars
# curl -O https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.0/spark-token-provider-kafka-0-10_2.12-3.5.0.jar
# && mv spark-token-provider-kafka-0-10_2.12-3.5.0.jar /opt/bitnami/spark/jars
# --packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0
# --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0
# mv spark-sql-kafka-0-10_2.12-3.5.0.jar /usr/local/spark/jars