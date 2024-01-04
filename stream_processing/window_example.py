import argparse
import json
import os
import random
import sys
from datetime import datetime
from typing import Iterable

from pyflink.common import Encoder, Time, Types, WatermarkStrategy
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.typeinfo import Types
from pyflink.common.watermark_strategy import (TimestampAssigner,
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

JARS_PATH = f"/home/dunghoang300699/Downloads/mlops/module2/feature-store/jar-files/data_ingestion/kafka_connect/jars/"  # Edit path to jar-files folder


class CountWindowProcessFunction(ProcessWindowFunction[tuple, tuple, str, TimeWindow]):
    def process(
        self,
        key: str,
        context: ProcessWindowFunction.Context[TimeWindow],
        elements: Iterable[tuple],
    ) -> Iterable[tuple]:
        print("hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
        return [("hihi", len([e for e in elements]))]


class CustomTimestampAssigner(TimestampAssigner):
    def extract_timestamp(self, element, record_timestamp) -> int:
        element = json.loads(element[0])
        timestamp = int(element["created"])
        return timestamp


if __name__ == "__main__":
    env = StreamExecutionEnvironment.get_execution_environment()

    env.add_jars(
        f"file://{JARS_PATH}/flink-connector-kafka-1.17.1.jar",
        f"file://{JARS_PATH}/kafka-clients-3.4.0.jar",
    )

    kafka_consumer = env.from_collection(
        [
            (
                '{"created": "1698726273706", "content": "Hi", "pregnancies": 3, "glucose": 173, "bloodpressure": 82, "skinthickness": 31, "insulin": 504, "bmi": 57.24939633955284, "diabetespedigreefunction": 1.0829519688016096, "age": 22}',
                1,
            ),
            (
                '{"created": "1698726273712", "content": "Hi", "pregnancies": 14, "glucose": 163, "bloodpressure": 28, "skinthickness": 6, "insulin": 669, "bmi": 4.595107929127025, "diabetespedigreefunction": 0.22109101869698378, "age": 71}',
                2,
            ),
            (
                '{"created": "1698726273718", "content": "Hi", "pregnancies": 2, "glucose": 138, "bloodpressure": 72, "skinthickness": 74, "insulin": 614, "bmi": 43.45136158935932, "diabetespedigreefunction": 0.9356038563293189, "age": 28}',
                3,
            ),
            (
                '{"created": "1698726273724", "content": "Hi", "pregnancies": 8, "glucose": 91, "bloodpressure": 119, "skinthickness": 0, "insulin": 143, "bmi": 49.31656497892159, "diabetespedigreefunction": 0.27572954812524736, "age": 69}',
                4,
            ),
            (
                '{"created": "1698726273730", "content": "Hi", "pregnancies": 1, "glucose": 143, "bloodpressure": 80, "skinthickness": 2, "insulin": 435, "bmi": 49.77976728186214, "diabetespedigreefunction": 0.8887816589275824, "age": 29}',
                5,
            ),
            (
                '{"created": "1698726273736", "content": "Hi", "pregnancies": 14, "glucose": 140, "bloodpressure": 76, "skinthickness": 73, "insulin": 410, "bmi": 58.09018829864623, "diabetespedigreefunction": 0.23754182850611483, "age": 51}',
                8,
            ),
            (
                '{"created": "1698726273742", "content": "Hi", "pregnancies": 13, "glucose": 47, "bloodpressure": 39, "skinthickness": 94, "insulin": 167, "bmi": 10.0757078142225, "diabetespedigreefunction": 1.590070627393116, "age": 50}',
                9,
            ),
            (
                '{"created": "1698726273748", "content": "Hi", "pregnancies": 6, "glucose": 7, "bloodpressure": 7, "skinthickness": 78, "insulin": 512, "bmi": 20.180598924772237, "diabetespedigreefunction": 0.09947635699105102, "age": 65}',
                15,
            ),
        ],
        type_info=Types.TUPLE([Types.STRING(), Types.INT()]),
    )

    watermark_strategy = (
        WatermarkStrategy.for_monotonous_timestamps().with_timestamp_assigner(
            CustomTimestampAssigner()
        )
    )

    ds = (
        kafka_consumer.assign_timestamps_and_watermarks(watermark_strategy)
        .key_by(lambda x: json.loads(x[0])["content"], key_type=Types.STRING())
        .window(TumblingEventTimeWindows.of(Time.milliseconds(20)))
        .process(
            CountWindowProcessFunction(), Types.TUPLE([Types.STRING(), Types.INT()])
        )
    )

    ds.print()

    env.execute()
