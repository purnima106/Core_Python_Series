print("Starting program...")

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Test").getOrCreate()

print("Spark session created")

df = spark.read.csv(
    "C:\\Users\\purni\\Desktop\\Core_Python_Series\\Data_and_Services\\Custom.csv",
    header=True,
    inferSchema=True
)

print("Data loaded")

df.show()

print("Finished")