import json
import os

import numpy as np
import pandas as pd
import requests
from confluent_kafka import Consumer, KafkaException


def main():
    consumer = Consumer(
        {
            "bootstrap.servers": "localhost:9092",
            "group.id": "mygroup",
            "auto.offset.reset": "latest",  # try latest to get the recent value
        }
    )

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    consumer.subscribe(["dunghc.public.sink_diabetes"])

    # Read messages from Kafka
    try:
        while True:
            # Wait for up to 1 second for new messages to arrive
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                # Parse data from our message
                value = json.loads(msg.value().decode("utf-8"))["data"]
                print(f"Received message: {value}")
                response = requests.post(
                    "http://localhost:4001/predict", headers=headers, json=value
                )
                if response.status_code == 200:
                    print("Successful!")
                    print("API response: ", response.json())
                else:
                    print("Failed to get prediction!")

                # Save new data to a csv file
                # features = list(value.keys())
                # features_value = np.array([[item] for item in value.values()])
                # print(len(features))
                # print(len(features_value))
                # print(features)
                # print(features_value)
                dic = {"Diabetes": 1, "Normal": 0}
                value["Outcome"] = dic[response.json()["result"]]
                if os.path.exists("./data/diabetes-kafka/diabetes_new.csv"):
                    df = pd.read_csv("./data/diabetes-kafka/diabetes_new.csv")
                    new_df = pd.DataFrame(value, index=[0])
                    pd.concat([df, new_df]).to_csv(
                        "./data/diabetes-kafka/diabetes_new.csv", index=False
                    )
                else:
                    df = pd.DataFrame(value, index=[0])
                    df.to_csv("./data/diabetes-kafka/diabetes_new.csv", index=False)

    except KeyboardInterrupt:
        print("Aborted by user!\n")

    finally:
        # Close consumer
        consumer.close()


if __name__ == "__main__":
    main()
