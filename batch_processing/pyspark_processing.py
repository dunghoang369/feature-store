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
    normalized_features = [
        "Pregnancies",
        "BloodPressure",
        "SkinThickness",
        "Insulin",
        "Age",
    ]
    for i, parquet_file in enumerate(parquet_files):
        df = spark.read.parquet(parquet_file)
        # Check null value of dataframe
        df.printSchema()
        for feature in normalized_features:
            # Convert column to vector type
            vector_assembler = VectorAssembler(
                inputCols=[feature], outputCol=f"{feature}_vect"
            )

            # Initialize min-max scaler
            scaler = MinMaxScaler(
                inputCol=f"{feature}_vect", outputCol=f"{feature}_normed"
            )

            # Add 2 processes to pipeline to transform dataframe
            pipeline = Pipeline(stages=[vector_assembler, scaler])
            df = (
                pipeline.fit(df)
                .transform(df)
                .withColumn(f"{feature}_normed", unlist(f"{feature}_normed"))
                .drop(f"{feature}_vect", feature)
            )
            df.show()

        df.printSchema()
        df_pandas = pd.DataFrame(df.toPandas())
        df_pandas.to_csv("test.csv")