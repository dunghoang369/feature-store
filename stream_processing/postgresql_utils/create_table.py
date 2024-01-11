import os
from glob import glob

import pandas as pd
from dotenv import load_dotenv
from postgresql_client import PostgresSQLClient

load_dotenv()


def main():
    pc = PostgresSQLClient(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    # Create devices table
    create_table_query = """
        CREATE TABLE IF NOT EXISTS diabetes_new (
            Created VARCHAR(30),
            Content VARCHAR(30),
            Pregnancies INT,
            Glucose INT,
            BloodPressure INT,
            SkinThickness INT,
            Insulin INT,
            BMI FLOAT,
            DiabetesPedigreeFunction FLOAT,
            Age INT
        );
    """
    try:
        pc.execute_query(create_table_query)
    except Exception as e:
        print(f"Failed to create table with error: {e}")


if __name__ == "__main__":
    main()
