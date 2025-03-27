from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json

def read_stream():
    pass

def create_bucket():
    pass

def write_bucket():
    pass

def main():
    # config spark session
    spark = SparkSession.builder \
        .appName("KafkaToMinIO") \
        .config("spark.executor.memory", "4g") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()
        
    # read_stream
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "my-connect-configs") \
        .option("startingOffsets", "earliest") \
        .option("maxOffsetsPerTrigger", "1") \
        .load()

    df.printSchema()

    df = df.select(col("key").cast("string"),col("value").cast("string"),"topic","partition","offset","timestamp","timestampType")

    query = df.writeStream \
    .outputMode("append") \
    .format("memory") \
    .queryName("kafka_results") \
    .start()
    # query = df.writeStream \
    # .outputMode("append") \
    # .format("memory") \
    # .queryName("kafka_results") \
    # .start()
    # query = df.writeStream \
    # .outputMode("append") \
    # .format("memory") \
    # .queryName("kafka_results") \
    # .start()

    import time
    time.sleep(90)

    print("printing df...")
    spark.sql("SELECT * FROM kafka_results").show()

    query.awaitTermination()

    # write_bucket
    # query = df.writeStream \
    #     .format("parquet") \
    #     .option("path", "s3a://brazilianecom/orders") \
    #     .option("checkpointLocation", "s3a://brazilianecom/checkpoint") \
    #     .start()
    # json_string_df = df.select(
    #     col("value").cast("string").alias("json_string")
    #     )

    spark.stop()
    

if __name__ == "__main__":
    main()
        # "org.apache.hadoop:hadoop-aws:3.3.0") \
# .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
# .config("spark.hadoop.fs.s3a.access.key", "root") \
# .config("spark.hadoop.fs.s3a.secret.key", "rootpassword") \
# .config("spark.hadoop.fs.s3a.path.style.access", "true") \