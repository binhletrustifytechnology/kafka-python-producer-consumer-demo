# 'bootstrap.servers': "kafka:9092",
# 'bootstrap.servers': "host.docker.internal:29092",
# 'bootstrap.servers': "kafka-broker:9092", # for kubernetes
# 'bootstrap.servers': "localhost:29092",
# 'bootstrap.servers': "localhost:9092",

from confluent_kafka import Consumer, KafkaException, KafkaError
import sys

conf = {
    # 'bootstrap.servers': "kafka-broker:9092",
    'bootstrap.servers': "kafka-service:9092",
    'group.id': "my-topic",
    'auto.offset.reset': 'smallest'
}

consumer = Consumer(**conf)

running = True


def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)
        print('subscribed')
        sys.stdout.flush()
        while running:
            msg = consumer.poll(5.0)
            # print('polled')
            sys.stdout.flush()
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                print(msg.value())
                sys.stdout.flush()
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


if __name__ == "__main__":
    basic_consume_loop(consumer, ['my-topic'])
