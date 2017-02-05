from kafka import KafkaConsumer
from config import eventador_config
import uuid
import json

brokers = eventador_config.brokers
consumer = KafkaConsumer(bootstrap_servers=brokers,
                         auto_offset_reset='largest',
                         value_deserializer=lambda m: json.loads(m, encoding='utf-8'),
                         group_id=uuid.uuid4())


consumer.subscribe(["tweets"])

max = 10
consumer.poll(max_records=max)
msg_consumed_max = 0

for msg in consumer:
    msg_consumed_max += 1
    print(msg.key, msg.value)

    if msg_consumed_max >= max:
        break


consumer.close()