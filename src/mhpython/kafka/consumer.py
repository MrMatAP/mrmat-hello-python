#  MIT License
#
#  Copyright (c) 2025 Mathieu Imfeld
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import typing
import uuid
import argparse

import kafka
import kafka.errors

from mhpython import __version__
from .record import DataclassRecord


class ConsumerRebalanceMonitor(kafka.ConsumerRebalanceListener):
    def __init__(self, consumer: kafka.KafkaConsumer = None):
        super().__init__()
        self._consumer = consumer

    def on_partitions_revoked(self, revoked: typing.Set[kafka.TopicPartition]):
        for partition in revoked:
            print(f'Revoked partition {partition.partition}')

    def on_partitions_assigned(self, assigned: typing.Set[kafka.TopicPartition]):
        for partition in assigned:
            offset = self._consumer.committed(partition)
            print(
                f'Assigned partition {partition.partition} with last committed offset {offset}'
            )


def main() -> int:
    parser = argparse.ArgumentParser(f'Kafka Consumer -- {__version__}')
    parser.add_argument(
        '--bootstrap',
        dest='bootstrap',
        required=False,
        default=['localhost:29092', 'localhost:39902', 'localhost:49902'],
        help='Kafka bootstrap server',
    )
    parser.add_argument(
        '--topic',
        type=str,
        dest='topic',
        required=False,
        default='records',
        help='Kafka topic to consume from',
    )
    parser.add_argument(
        '--client-id',
        dest='client_id',
        required=False,
        default=f'mhpython-kafka-consumer-{uuid.uuid4()}',
        help='Kafka client ID',
    )
    parser.add_argument(
        '--group-id',
        dest='group_id',
        required=False,
        default='records-group',
        help='Kafka group ID',
    )
    args = parser.parse_args()

    consumer = None
    try:
        #
        # Create a consumer

        consumer = kafka.KafkaConsumer(
            args.topic,
            bootstrap_servers=args.bootstrap,
            client_id=args.client_id,
            group_id=args.group_id,
            group_instance_id=args.client_id,
            key_deserializer=DataclassRecord.deserialize_key,
            value_deserializer=DataclassRecord.deserialize,
        )
        if consumer.bootstrap_connected():
            print('Consumer is connected')
        consumer.subscribe([args.topic], listener=ConsumerRebalanceMonitor(consumer))
        print(f'Consumer is subscribed to topic {args.topic}')

        #
        # Consume messages

        for msg in consumer:
            print(msg.value)

        return 0
    except KeyboardInterrupt:
        print('Consumer is shutting down normally')
        return 0
    except kafka.errors.IllegalStateError as ise:
        print(f'consumer.subscribe must not happen after consumer.assign: {ise}')
        return 1
    except AssertionError as ae:
        print(
            f'AssertionError: Neither topics nor pattern to subscribe is provided: {ae}'
        )
        return 1
    except TypeError as te:
        print(f'ConsumerRebalanceListener is not of the correct type: {te}')
        return 1
    finally:
        if consumer is not None:
            metrics = consumer.metrics()
            print(
                f'This consumer had a request rate of {metrics.get("consumer-metrics", {}).get("request-rate")}.'
            )
            consumer.close()


if __name__ == '__main__':
    sys.exit(main())
