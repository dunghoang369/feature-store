import os
import random
import shutil

import pandas as pd
from helpers import load_cfg

if __name__ == "__main__":
    # Define data features
    features = [
        "Pregnancies",
        "Glucose",
        "BloodPressure",
        "SkinThickness",
        "Insulin",
        "BMI",
        "DiabetesPedigreeFunction",
        "Age",
        "Outcome",
    ]

    for i in range(10):
        df = pd.DataFrame()
        j = 11
        while j < 1000000:
            new_row = {}
            for feature in features:
                if feature == "Pregnancies":
                    new_row[feature] = random.randint(0, 17)
                elif feature == "Glucose":
                    new_row[feature] = random.randint(0, 199)
                elif feature == "BloodPressure":
                    new_row[feature] = random.randint(0, 122)
                elif feature == "SkinThickness":
                    new_row[feature] = random.randint(0, 99)
                elif feature == "Insulin":
                    new_row[feature] = random.randint(0, 846)
                elif feature == "DiabetesPedigreeFunction":
                    new_row[feature] = random.uniform(0.078000, 2.420000)
                elif feature == "BMI":
                    new_row[feature] = random.uniform(0.0, 67.1)
                elif feature == "Age":
                    new_row[feature] = random.randint(21, 81)
                else:
                    new_row[feature] = random.randint(0, 1)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            j += 1
        # Save dataframe into csv files
        print(df)
        df.to_csv(f"../../data/diabetes/diabetes_{str(i+1)}.csv", index=False)
