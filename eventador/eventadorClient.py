import eventadorProducer as ev
import eventadorConsumer as ec

#Setup Eventador
class EventadorClient():
    """config object is a dict containing
        {
            "brokers": "brokers",
            "topic"  : "topic",
            "bucket" : "bucket",
            "max_records" : max
            "publisher": publisher # some kind of backend publisher i.e. s3, elasticsearch, etc
        }
    """
    def __init__(self, config):
        self.config = config
        self.producer = ev.EventadorProducer(self.config['brokers'], self.config['topic'])
        self.publisher = self.createPublisher()

    def createPublisher(self):
        publisher_type = self.config['publisher']
        if publisher_type is not None:
            if publisher_type == 's3':
                return ec.S3Publisher(self.config)

        return None

    def get_producer_and_publisher(self):
        return self.producer, self.publisher
