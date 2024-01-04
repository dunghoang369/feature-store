import argparse
import json
import os
import random
import sys
from datetime import datetime
from time import sleep
from typing import Iterable

from bson import json_util
from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic
from pyflink.common import Encoder, Time, Types, WatermarkStrategy
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.common.watermark_strategy import (Duration, TimestampAssigner,
                                               WatermarkStrategy)
from pyflink.datastream import (ProcessWindowFunction,
                                StreamExecutionEnvironment)
from pyflink.datastream.connectors import FlinkKafkaConsumer
from pyflink.datastream.connectors.file_system import (FileSink,
                                                       OutputFileConfig,
                                                       RollingPolicy)
from pyflink.datastream.connectors.kafka import (
    KafkaOffsetsInitializer, KafkaRecordSerializationSchema, KafkaSink,
    KafkaSource)
from pyflink.datastream.window import TimeWindow, TumblingEventTimeWindows

cache = []
JARS_PATH = f"/home/dunghoang300699/Downloads/mlops/module2/feature-store/jar-files/data_ingestion/kafka_connect/jars/"  # Edit path to jar-files folder


class CountWindowProcessFunction(ProcessWindowFunction[tuple, tuple, str, TimeWindow]):
    def process(
        self,
        key: str,
        context: ProcessWindowFunction.Context[TimeWindow],
        elements: Iterable[tuple],
    ) -> Iterable[tuple]:
        print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
        for e in elements:
            print("------------------------------------------")
            record = json.loads(e)
            data = record["payload"]["after"]
            # print(data)
            # producer.send(topic_name, json.dumps(e, default=json_util.default).encode("utf-8"))
            # sleep(2)
            # cache.append(data)
            print(data)
        return [json.dumps({"data": {"1": 1, "2": 2}})]


class CustomTimestampAssigner(TimestampAssigner):
    def extract_timestamp(self, element, record_timestamp) -> int:
        element = json.loads(element)
        # date_format = "%d/%m/%Y %H:%M:%S"
        # print("created: ", element["payload"]["after"]["created"])
        # timestamp = int(datetime.strptime(element["payload"]["after"]["created"], date_format).timestamp()) * 1000
        timestamp = int(element["payload"]["after"]["created"])
        print("timestamp:", timestamp)
        print("--------------------------------")
        return timestamp


if __name__ == "__main__":
    servers = "localhost:9092"
    producer = KafkaProducer(bootstrap_servers=servers)
    admin = KafkaAdminClient(bootstrap_servers=servers)
    topic_name = "dunghc.public.sink_window_datastream"
    if topic_name not in admin.list_topics():
        topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
        admin.create_topics([topic])

    # for _ in range(1000):
    # # Randomize values for feature columns
    #     record = {}
    #     record["Pregnancies"] = random.randint(0, 17)
    #     record["Glucose"] = random.randint(0, 199)
    #     producer.send(
    #         topic_name, json.dumps(record, default=json_util.default).encode("utf-8")
    #     )
    #     sleep(2)

    env = StreamExecutionEnvironment.get_execution_environment()

    env.add_jars(
        f"file://{JARS_PATH}/flink-connector-kafka-1.17.1.jar",
        f"file://{JARS_PATH}/kafka-clients-3.4.0.jar",
    )

    sink = (
        KafkaSink.builder()
        .set_bootstrap_servers("http://localhost:9092")
        .set_record_serializer(
            KafkaRecordSerializationSchema.builder()
            .set_topic("dunghc.public.sink_window_diabetes")
            .set_value_serialization_schema(SimpleStringSchema())
            .build()
        )
        .build()
    )

    kafka_consumer = FlinkKafkaConsumer(
        topics="dunghc.public.diabetes_new",
        properties={"bootstrap.servers": "localhost:9092", "group.id": "test_group"},
        deserialization_schema=SimpleStringSchema(),
    )

    watermark_strategy = (
        WatermarkStrategy.for_monotonous_timestamps()
        .with_timestamp_assigner(CustomTimestampAssigner())
        .with_idleness(Duration.of_seconds(30))
    )

    stream = env.add_source(kafka_consumer)
    ds = (
        stream.assign_timestamps_and_watermarks(watermark_strategy)
        .key_by(
            lambda x: json.loads(x)["payload"]["after"]["content"],
            key_type=Types.STRING(),
        )
        .window(TumblingEventTimeWindows.of(Time.milliseconds(10000)))
        .process(CountWindowProcessFunction(), output_type=Types.STRING())
        .sink_to(sink=sink)
        .set_parallelism(1)
    )

    # ds.print()
    env.execute()
