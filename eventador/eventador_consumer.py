from __future__ import print_function
from kafka import KafkaConsumer
from config import s3conn
from config import esconn
from elasticsearch import helpers
import json
import uuid


class BaseEventadorConsumer(object):
    def __init__(self, config):
        self.config = config
        self.consumer = KafkaConsumer(bootstrap_servers=self.config['brokers'],
                                      value_deserializer=lambda s: json.loads(s, encoding='utf-8'),
                                      auto_offset_reset="largest",
                                      group_id=uuid.uuid4())
        self.subscribe()

    def subscribe(self):
        self.consumer.subscribe(self.config['topic'])

    def poll(self):
        self.consumer.poll(max_records=self.config['max_records'])

    def collect(self, key):
        self.poll()

        collected = 0
        for msg in self.consumer:
            collected += 1

            if msg.key == key:
                yield msg.value

            if collected >= self.config['max_records']:
                self.close()
                break

    def close(self):
        self.consumer.close()


# Can create additional publishers that inherit from BaseEventador consumer need a publish method and a collect method
class S3Publisher(BaseEventadorConsumer):
    def __init__(self, config):
        super(self.__class__, self).__init__(config)

    def publish(self, key):
        try:
            bucket = self.config['bucket']
            s3conn.write_file_to_s3(json.dumps([doc for doc in self.collect(key)]), key, bucket)

            print('{} written to {} bucket'.format(key, bucket))
        except Exception as ex:
            print(str(ex))


class ElasticSearchPublisher(BaseEventadorConsumer):
    def __init__(self, config):
        super(self.__class__, self).__init__(config)

    def publish(self, key):
        def docs_gen(docs):
            for doc in docs:
                index_dict = {
                    '_index': self.config['index'],
                    '_type': self.config['doc_type'],
                    '_source': doc
                }
                yield index_dict

        try:
            es = esconn.esconn()
            stats = helpers.bulk(es, docs_gen(self.collect(key)), stats_only=True)
            print("{} messages indexed to elasticsearch".format(stats[0]))
        except Exception as ex:
            print(str(ex))
