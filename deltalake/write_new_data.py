import random

import numpy as np
import pandas as pd

from deltalake import DeltaTable
from deltalake.writer import write_deltalake

# Load Delta Lake table
print("*" * 80)
dt = DeltaTable("../data/diabetes-deltalake/diabetes_1")
print("Current Delta table:")
print(dt.to_pandas())
df = pd.DataFrame()
j = 0
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
while j < 1000:
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
        else:
            new_row[feature] = random.randint(21, 81)

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    j += 1
# Append to create new versions
# Take a look at this for more details: https://delta.io/blog/2022-10-15-version-pandas-dataset/
write_deltalake(dt, df, mode="append")
print("Final Delta table:")
dt2 = DeltaTable("../data/diabetes-deltalake/diabetes_1")
print(dt2.to_pandas())
