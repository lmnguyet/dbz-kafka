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
        .config("spark.jars.packages", 
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0") \
        .config("spark.jars.repositories", "https://repo1.maven.org/maven2") \
                # "org.apache.hadoop:hadoop-aws:3.3.0") \
        # .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
        # .config("spark.hadoop.fs.s3a.access.key", "root") \
        # .config("spark.hadoop.fs.s3a.secret.key", "rootpassword") \
        # .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .getOrCreate()
        
    # read_stream
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "dbserver1.brazilian_ecom.orders") \
        .option("startingOffsets", "earliest") \
        .load()
    

    # create_bucket


    # write_bucket
    # query = df.writeStream \
    #     .format("parquet") \
    #     .option("path", "s3a://brazilianecom/orders") \
    #     .option("checkpointLocation", "s3a://brazilianecom/checkpoint") \
    #     .start()
    json_string_df = df.select(
        col("value").cast("string").alias("json_string")
        )

    query = json_string_df.writeStream \
        .format("console") \        
        .outputMode("append") \        
        .option("truncate", "false") \ 
        .start()

    

    query.awaitTermination()

if __name__ == "__main__":
    main()