# dbz-kafka

This repository builds a basic flow to ingest and synchronize data from a MySQL database to a MinIO Delta Table. The application is built on Docker with Debezium and Spark.

![](overal-flow.png)

## Prerequisites
WSL version: 
Docker version:
[Read: Installing Docker on WSL](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

## Dataset
This project uses the Pixar Films dataset from [Maven Analytics](https://mavenanalytics.io/data-playground).

## Set up docker services
1. MySQL
MySQL 8.0
Database: pixal_films
Check if the database is built successfully:
```docker exec -it mysql mysql -u <your database user> -p -D pixar_films```

```mysql> show tables;```
```mysql> select * from films;```

2. MinIO
MinIO UI: ```localhost:9001```

3. Kafka
- ZooKeeper 3.0
- Kafka 3.0
- Kafka UI: ```localhost:9089```

4. Kafka Connect with Debezium
Debezium 3.0

5. Spark
- Spark Master 3.5
- Spark Worker 3.5
- Spark UI: ```localhost:8080```
Note: You can manually download jar files as in spark/jars/jarsfiles or add this configuration in spark-default.conf as below:

spark.jars.packages                                 org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0

**All the jar libraries are version compatible with services used in this project.**

## Start
1. Run all docker services
```docker compose up -d``

2. Create a connector between MySQL and Kafka
- Check if Debezium is running: ```curl -H "Accept:application/json" localhost:8083/connectors/```
- Create a connector with the configuration file: ```curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d @mysql-connector.json```

3. Submit a Spark job to stream from Kafka to MinIO
```docker exec -u root -it spark-master bash```
```spark-submit /app/stream.py``