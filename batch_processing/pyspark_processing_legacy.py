window_example.py
import argparse
import os
from glob import glob

import dotenv
import pandas as pd
from pyspark.ml import Pipeline
from pyspark.ml.feature import MinMaxScaler, VectorAssembler
from pyspark.sql import Row, SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import DoubleType

dotenv.load_dotenv()

if __name__ == "__main__":
    # The entrypoint to access all functions of Spark
    spark = (
        SparkSession.builder.master("local[*]")
        .config("spark.driver.bindAddress", "localhost")
        .config("spark.ui.port", "4050")
        .appName("Python Spark read parquet example")
        .getOrCreate()
    )

    parquet_files = glob("../data/diabetes-deltalake/**/*.parquet", recursive=True)
    unlist = udf(lambda x: round(float(list(x)[0]), 3), DoubleType())

    for i, parquet_file in enumerate(parquet_files):
        df = spark.read.parquet(parquet_file)
        df.printSchema()  # check null value
        vector_assembler = VectorAssembler(
            inputCols=["Glucose"], outputCol="Glucose_vect"
        )
        df = vector_assembler.transform(df)
        scaler = MinMaxScaler(inputCol="Glucose_vect", outputCol="Glucose_normed")
        model = scaler.fit(df)
        df = model.transform(df)
        df = df.withColumn("Glucose_normed_unlist", unlist("Glucose_normed"))
        df.drop("Glucose", "Glucose_vect", "Glucose_normed").show()
        # for i in range(df.count()):
        #     row = df.collect[i]

        # print(df.collect()[0].__getitem__('Pregnancies'))
        # df.write.parquet(f"diabetes_{str(i+2)}.parquet")
        # df.printSchema()
        # df.select("Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Glucose_vect", "Glucose_normed", "Glucose_normed_unlist")\
        # .write.format("jdbc")\
        # .option("driver", "org.postgresql.Driver")\
        # .option("user", os.getenv("POSTGRES_USER"))\
        # .option("password", os.getenv("POSTGRES_PASSWORD"))\
        # .option("url", "jdbc:postgresql://127.0.0.1:5432/k6")\
        # .option("dbtable", "diabetes")\
        # .save()
        # print("Insert table to postgresql")
        break
    # print(os.getenv("POSTGRES_DB"))
    # print(os.getenv("POSTGRES_USER"))
    # print(os.getenv("POSTGRES_PASSWORD"))
    # print(os.getenv("POSTGRES_HOST"))
    # print(os.getenv("POSTGRES_PORT"))
