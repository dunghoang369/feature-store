import os
from datetime import datetime
from glob import glob

import catboost as cb
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, classification_report,
                             fbeta_score, make_scorer, precision_score,
                             recall_score)
from sklearn.model_selection import train_test_split

storage_source = "/training/data/diabetes/*.csv"
kafka_source = "/training/data/diabetes-kafka/*.csv"


def fbeta(y_true, y_predict):
    ## Function used to calculate f_beta score
    return fbeta_score(y_true, y_predict, beta=np.sqrt(5))


def metrics(y_true, y_predict):
    ## Metrics used to evaluate models
    accuracy = accuracy_score(y_true, y_predict)
    precision = precision_score(y_true, y_predict)
    recall = recall_score(y_true, y_predict)
    f_score = fbeta(y_true, y_predict)

    return accuracy, precision, recall, f_score


def display_metrics(accuracy, precision, recall, fbeta_score):
    ## Show metric results to screen
    print(f"Accuracy: {accuracy:.5f}")
    print(f"Precision: {precision:.5f}")
    print(f"Recall: {recall:.5f}")
    print(f"Fbeta_score: {fbeta_score:.5f}")


if __name__ == "__main__":
    final_data_df = pd.DataFrame()
    file_paths = glob(storage_source) + glob(kafka_source)
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        final_data_df = pd.concat([final_data_df, df])

    data_train, data_test = train_test_split(
        final_data_df, test_size=0.1, random_state=42
    )
    y_train = data_train.pop("Outcome")
    y_test = data_test.pop("Outcome")

    print(
        f"Data train: X_train shape {data_train.shape}, y_train shape {y_train.shape}"
    )
    print(f"Data test: X_test shape {data_test.shape}, y_test shape {y_test.shape}")

    catboost_hyperparameters = {
        "loss_function": "Logloss",
        "learning_rate": 0.078560234869898,
        "iterations": 1000,
        "depth": 4,
        "bagging_temperature": 9,
        "border_count": 233,
        "grow_policy": "SymmetricTree",
        "l2_leaf_reg": 8.13759140001093,
        "min_data_in_leaf": 19,
        "random_strength": 2.0521447931933214,
        "rsm": 0.48665862445945,
    }

    catboost = cb.CatBoostClassifier(**catboost_hyperparameters)
    catboost.fit(data_train, y_train)
    y_predict = catboost.predict(data_test)
    accuracy, precision, recall, f_score = metrics(y_test, y_predict)
    display_metrics(accuracy, precision, recall, f_score)
    print(classification_report(y_pred=y_predict, y_true=y_test))
    created = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
    joblib.dump(catboost, f"/training/models/{created}.pkl")
