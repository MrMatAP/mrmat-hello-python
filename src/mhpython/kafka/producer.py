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
import time
import uuid
import argparse

import kafka
import kafka.errors

from mhpython import __version__
from .record import DataclassRecord, RegionEnum


def main() -> int:
    parser = argparse.ArgumentParser(f'Kafka Producer -- {__version__}')
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
        help='Kafka topic',
    )
    parser.add_argument(
        '--client-id',
        dest='client_id',
        required=False,
        default=f'mhpython-kafka-producer-{uuid.uuid4()}',
        help='Kafka client ID',
    )
    parser.add_argument(
        '--transactional-id',
        dest='transaactional_id',
        required=True,
        help='Kafka client transactional ID',
    )
    parser.add_argument(
        '--region',
        dest='region',
        type=RegionEnum,
        choices=list(RegionEnum),
        required=True,
        help='Region of the record to produce',
    )
    args = parser.parse_args()

    admin = None
    producer = None
    try:
        #
        # Create a topic if it does not exist

        admin = kafka.KafkaAdminClient(
            bootstrap_servers=args.bootstrap, client_id=args.client_id
        )
        topic = kafka.admin.NewTopic(
            name=args.topic, num_partitions=len(RegionEnum), replication_factor=2
        )
        try:
            admin.create_topics([topic])
        except kafka.errors.TopicAlreadyExistsError:
            print(f'Topic {args.topic} already exists, not recreating it')

        #
        # Create a producer

        producer = kafka.KafkaProducer(
            bootstrap_servers=args.bootstrap,
            client_id=args.client_id,
            transactional_id=args.transaactional_id,
            key_serializer=DataclassRecord.serialize_key,
            value_serializer=DataclassRecord.serialize,
            acks='all',
        )
        if producer.bootstrap_connected():
            print('Producer is connected')
        producer.init_transactions()
        print('Transactions are initialized')

        #
        # Send records

        while True:
            rec = DataclassRecord(region=args.region)
            producer.begin_transaction()
            producer.send(topic=topic.name, key=rec.region, value=rec)
            producer.commit_transaction()
            print(f'Record sent: {rec}')
            time.sleep(1)

    except KeyboardInterrupt:
        print('Producer is shutting down normally')
        return 0
    except kafka.errors.ProducerFencedError as kpfe:
        print(
            f'ProducerFencedError: if another producer with the same transactional_id is active: {kpfe}'
        )
        return 1
    except kafka.errors.KafkaTimeoutError as kte:
        print(
            f'KafkaTimeoutError: if the time taken for initialize the transaction has surpassed max.block.ms. {kte}'
        )
        return 1
    except kafka.errors.IllegalStateError as kise:
        print(f'IllegalStateError: No transactional_id is configured: {kise}')
        return 1
    except kafka.errors.AuthorizationError as kae:
        print(
            f'AuthorizationError: fatal error indicating that the configured transactional_id is not authorized {kae}'
        )
        return 1
    except kafka.errors.KafkaError as ke:
        print(f'KafkaError: {ke}')
        return 1
    except TypeError as te:
        print(f'Topic is not a string: {te}')
        return 1
    except ValueError as ve:
        print(f'Topic is invalid: {ve}')
        return 1
    except AssertionError as ae:
        print(
            f'AssertionError: KafkaProducer is closed or key and value are both None: {ae}'
        )
        return 1
    finally:
        if admin is not None:
            admin.close()
        if producer is not None:
            metrics = producer.metrics()
            print(
                f'This producer had a request rate of {metrics.get("producer-metrics", {}).get("request-rate")}.'
            )
            producer.close()


if __name__ == '__main__':
    sys.exit(main())
