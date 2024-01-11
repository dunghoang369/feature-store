import os
import random
from datetime import datetime
from time import sleep

from dotenv import load_dotenv
from postgresql_client import PostgresSQLClient
from tqdm import trange

load_dotenv()

TABLE_NAME = "diabetes_new"
NUM_ROWS = 1000


def main():
    pc = PostgresSQLClient(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    # Features of diabetes table
    features = [
        "Pregnancies",
        "Glucose",
        "BloodPressure",
        "SkinThickness",
        "Insulin",
        "BMI",
        "DiabetesPedigreeFunction",
        "Age",
    ]

    # Loop over all columns and create random values
    for _ in trange(NUM_ROWS):
        # Randomize values for feature columns
        feature_values = []
        for feature in features:
            if feature == "Pregnancies":
                feature_values.append(str(random.randint(0, 17)))
            elif feature == "Glucose":
                feature_values.append(str(random.randint(0, 199)))
            elif feature == "BloodPressure":
                feature_values.append(str(random.randint(0, 122)))
            elif feature == "SkinThickness":
                feature_values.append(str(random.randint(0, 99)))
            elif feature == "Insulin":
                feature_values.append(str(random.randint(0, 846)))
            elif feature == "DiabetesPedigreeFunction":
                feature_values.append(str(random.uniform(0.078000, 2.420000)))
            elif feature == "BMI":
                feature_values.append(str(random.uniform(0.0, 67.1)))
            else:
                feature_values.append(str(random.randint(21, 81)))
        # Add device_id and current time
        data = [str(round(datetime.now().timestamp() * 1000)), "Hi"] + feature_values
        # Insert data
        query = f"""
            insert into {TABLE_NAME} ({",".join(["Created", "Content"] + features)})
            values {tuple(data)}
        """
        pc.execute_query(query)
        sleep(2)
    print("Done process")


if __name__ == "__main__":
    main()
    # print(str(round(datetime.now().timestamp()*1000)))
