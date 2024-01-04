import os
import shutil
from glob import glob

import pandas as pd
from helpers import load_cfg

from deltalake.writer import write_deltalake

CFG_PATH = "../utils/config.yaml"

if __name__ == "__main__":
    # Load config.yaml
    cfg = load_cfg(CFG_PATH)

    # Get csv files
    csv_files = glob("../data/diabetes/*.csv")

    # Write data into deltalake format
    for csv_file in csv_files:
        file_name = csv_file.split("/")[-1].split(".")[0]
        df = pd.read_csv(csv_file)
        if os.path.exists(
            os.path.join(cfg["datastore"]["diabetes_deltalake_path"], file_name)
        ):
            shutil.rmtree(
                os.path.join(cfg["datastore"]["diabetes_deltalake_path"], file_name)
            )
        write_deltalake(
            os.path.join(cfg["datastore"]["diabetes_deltalake_path"], file_name), df
        )
        print(f"Generated the file {file_name} successfully!")

    df = pd.read_csv("../data/diabetes/diabetes.csv")
    write_deltalake("../data/diabetes-deltalake/diabetes", df)
