from kafka import KafkaConsumer
from config import eventador_config
import uuid
import json

brokers = eventador_config.brokers
consumer = KafkaConsumer(bootstrap_servers=brokers,
                         auto_offset_reset='smallest',
                         value_deserializer=lambda m: json.loads(m, encoding='utf-8'),
                         group_id=uuid.uuid4())


consumer.subscribe(["tweets"])

max_records = 1000
consumer.poll(max_records=max_records)
msg_consumed_count = 0

for msg in consumer:
    msg_consumed_count += 1
    print(msg_consumed_count, msg.value)

    if msg_consumed_count >= max_records:
        break


consumer.close()