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
        .appName("SpakApp") \
        .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore")\
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")\
        .getOrCreate()
        
    # read_stream
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "dbserver1.pixar_films.films") \
        .option("startingOffsets", "earliest") \
        .load()

    df.printSchema()

    df = df.selectExpr("CAST(value as STRING) as value_str", "value")
    # df = df.select(col("key").cast("string"),col("value").cast("string"),"topic","partition","offset","timestamp","timestampType")

    # query = df.writeStream \
    # .outputMode("append") \
    # .format("memory") \
    # .queryName("kafka_results") \
    # .start()

    # import time
    # time.sleep(90)

    # print("printing df...")
    # spark.sql("SELECT * FROM kafka_results").show(truncate=False)

    # query = df.writeStream \
    # .format("delta") \
    # .option("path", "s3a://test/films") \
    # .option("checkpointLocation", "s3a://test/checkpoints") \
    # .start()

    query = df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("path", "s3a://test/films") \
    .option("checkpointLocation", "s3a://test/checkpoints").start()

    df1 = spark.read.format("delta").load("s3a://test/films")
    print(df1)

    query.awaitTermination()

    spark.stop()
    

if __name__ == "__main__":
    main()
        # "org.apache.hadoop:hadoop-aws:3.3.0") \
# .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
# .config("spark.hadoop.fs.s3a.access.key", "root") \
# .config("spark.hadoop.fs.s3a.secret.key", "rootpassword") \
# .config("spark.hadoop.fs.s3a.path.style.access", "true") \