# Please refer to the following documentation for more information
# about Delta Lake: https://delta-io.github.io/delta-rs/python/usage.html
from deltalake import DeltaTable

# Load Delta Lake table
print("*" * 80)
dt = DeltaTable("../../data/diabetes-deltalake/diabetes_1")
# Uncomment the below line to switch to another version
dt.load_version(0)
# print("[INFO] Loaded Delta Lake table successfully!")

# Investigate Delta Lake table
print("*" * 80)
print("[INFO] Delta Lake table schema:")
print(dt.schema().json())
print("[INFO] Delta Lake table version:")
print(dt.version())
print("[INFO] Delta Lake files:")
print(dt.files())
print("[INFO] Delta Lake metadata:")
print(dt.metadata())

# Query some data
print("*" * 80)
print("[INFO] Delta Lake table data on pressure column:")
print(dt.to_pandas(columns=["BMI"]))


# Investigate history of actions performed on the table
print("*" * 80)
print("[INFO] History of actions performed on the table")
print(dt.history())
