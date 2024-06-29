import json
from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from src.config.config import KAFKA_HOST, CONSUMER_KAFKA_PRODUCT


class KafkaService:

    def delivery_report(self, err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def send_to_kafka(self, topic, data):
        conf = {
            'bootstrap.servers': KAFKA_HOST
        }

        producer = Producer(**conf)

        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')

        producer.produce(topic=topic, key=str(data['id']), value=json_data, callback=self.delivery_report)

        producer.poll(1)

        producer.flush()

    def consume_from_kafka(self, topic):
        conf = {
            'bootstrap.servers': KAFKA_HOST,
            'group.id': CONSUMER_KAFKA_PRODUCT,
            'auto.offset.reset': 'earliest'
        }

        consumer = Consumer(**conf)
        consumer.subscribe([topic])

        empty_poll_count = 0
        msg_list = []

        try:
            while empty_poll_count < 5:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    empty_poll_count += 1
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        print('%% %s [%d] reached end at offset %d\n' %
                                (msg.topic(), msg.partition(), msg.offset()))
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    empty_poll_count = 0
                    message_value = msg.value().decode('utf-8')
                    print('Received message: {}'.format(msg.value().decode('utf-8')))
                    msg_list.append(json.loads(message_value))

            return msg_list

        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()