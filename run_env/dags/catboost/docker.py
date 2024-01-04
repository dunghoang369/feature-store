from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

TRAINING_DIR = "/home/dunghoang300699/Downloads/mlops/module2/feature-store/run_env"
with DAG(
    dag_id="docker_cb", start_date=datetime(2023, 11, 10), schedule="0 0 1 * *"
) as dag:
    # This is often used to seperate environment dependencies
    # from other components
    train_task = DockerOperator(
        task_id="train_task",
        image="dunghoang99/airflow-cb-stage:0.0.1",
        container_name="airflow-cb-stage",
        api_version="auto",
        auto_remove=True,
        network_mode="bridge",
        docker_url="tcp://docker-proxy:2375",
        mounts=[
            Mount(
                source=f"{TRAINING_DIR}/dags/catboost",
                target="/training/code",
                type="bind",
            ),
            Mount(
                source=f"{TRAINING_DIR}/data",
                target="/training/data",
                type="bind",
            ),
            Mount(
                source=f"{TRAINING_DIR}/models", target="/training/models", type="bind"
            ),
        ],
        working_dir="/training",
        command="python code/train.py",
    )
