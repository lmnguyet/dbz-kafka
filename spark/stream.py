from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window
import time
from delta.tables import DeltaTable

# create spark session
spark = SparkSession.builder \
        .appName("SpakApp") \
        .getOrCreate()

delta_path = "s3a://test2/films"

# read stream from kafka
def read_stream():
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("subscribe", "dbserver1.pixar_films.films") \
        .option("startingOffsets", "earliest") \
        .option("failOnDataLoss", "false") \
        .load()
    return df

# process stream df
def process_stream(df):
    schema = StructType([
        StructField("payload", StructType([
            StructField("before", StructType([
                StructField("number", IntegerType(), nullable=False)
            ]))
            , StructField("after", StructType([
                StructField("number", IntegerType(), nullable=False),
                StructField("film", StringType(), nullable=False),
                StructField("release_date", DateType(), nullable=True),
                StructField("run_time", IntegerType(), nullable=True),
                StructField("film_rating", StringType(), nullable=True),
                StructField("plot", StringType(), nullable=True)
            ]))
            , StructField("op", StringType(), nullable=False)
            # , StructField("ts_ms", IntegerType(), nullable=False)
        ]))
    ])

    processed_df = df.select(from_json(col("value").cast("string"), schema).alias("parsed_value"))

    # window_spec = Window.partitionBy(
    #     when(col("parsed_value.payload.op") == "d", col("parsed_value.payload.before.number"))\
    #     .otherwise(col("parsed_value.payload.after.number"))
    # ).orderBy(desc("parsed_value.payload.ts_ms"))

    # processed_df = parsed_df.withColumn("row_num", row_number().over(window_spec)) \
    #     .filter("row_num = 1") \
    #     .drop("row_num")
    
    upsert_df = processed_df.select(\
            when(col("parsed_value.payload.op") == "d", col("parsed_value.payload.before.number")).otherwise(col("parsed_value.payload.after.number")), \
            col("parsed_value.payload.after.film"),\
            col("parsed_value.payload.after.release_date").cast("date"),\
            col("parsed_value.payload.after.run_time"),\
            col("parsed_value.payload.after.film_rating"),\
            col("parsed_value.payload.after.plot"),\
            col("parsed_value.payload.op")
        )
    # , col("parsed_value.payload.op"))
    return upsert_df

# create bucket and delta table if not exist
def create_bucket():
    pass

# write stream into delta table
def write_bucket():
    pass

# refresh query data from delta table
def refresh():
    while True:
        if DeltaTable.isDeltaTable(spark, delta_path):
            df = spark.read.format("delta").load(delta_path)
            print(f"Tổng số bản ghi: {df.count()}")
            df.show(40)
        else:
            print(f"Delta Table tại {delta_path} chưa tồn tại!")
        time.sleep(30)

def upsertToDelta(microBatchOutputDF, batchId):
    if not DeltaTable.isDeltaTable(spark, delta_path):
        print("Creating delta table ...")
        microBatchOutputDF.limit(0).write.format("delta").save(delta_path)

    delta_table = DeltaTable.forPath(spark, delta_path)
    
    (delta_table.alias("t").merge(
        microBatchOutputDF.alias("s"),
        "s.number = t.number")
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
        # .whenMatchedDelete("s.op = 'd'")
    )

def main():
        
    # read_stream
    df = read_stream()

    processed_df = process_stream(df)

    # spark.sql(f"""
    # CREATE TABLE IF NOT EXISTS delta.`s3a://test1/films` (
    #     number INT,
    #     film STRING,
    #     release_date DATE,
    #     run_time INT,
    #     film_rating STRING,
    #     plot STRING
    # ) USING DELTA
    # """)
    # delta_table = DeltaTable.forPath(spark, delta_path)

    query = processed_df.writeStream\
    .foreachBatch(upsertToDelta)\
    .option("checkpointLocation", "s3a://test2/checkpoints")\
    .outputMode("update")\
    .start()

    refresh()

    query.awaitTermination()

    spark.stop()
    

if __name__ == "__main__":
    main()
    # spark.sql("select * from delta.`s3a://test1/films`").show(40)
    # test()



        # "org.apache.hadoop:hadoop-aws:3.3.0") \
# .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
# .config("spark.hadoop.fs.s3a.access.key", "root") \
# .config("spark.hadoop.fs.s3a.secret.key", "rootpassword") \
# .config("spark.hadoop.fs.s3a.path.style.access", "true") \