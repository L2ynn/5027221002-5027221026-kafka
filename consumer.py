from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, FloatType

spark = SparkSession.builder \
    .appName("TemperatureAlert") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
    .getOrCreate()

schema = StructType() \
    .add("sensor_id", StringType()) \
    .add("temperature", FloatType())

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "sensor-suhu") \
    .load()

json_df = df.select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.sensor_id", "data.temperature")

alert_df = json_df.filter(col("temperature") > 80)

query = alert_df \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()
