import argparse
from pyspark.sql import SparkSession

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data")
    args = parser.parse_args()

    spark = SparkSession.builder.appName("ValueDetermination").getOrCreate()

    lines = spark.read.text(args.data).rdd.map(lambda r: r[0])

    print(lines.collect())

    spark.stop()
