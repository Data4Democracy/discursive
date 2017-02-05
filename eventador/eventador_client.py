import eventador_producer as eV
import eventador_consumer as eC


# Setup Eventador
class EventadorClient:
    def __init__(self, config):
        self.config = config  # subscribes to topic and publishes them somewhere else, here s3

    def get_publisher(self, config):
        type = config['publisher']

        if type is not None:
            if type == 's3':
                return eC.S3Publisher(config)
            elif type == 'es':
                return eC.ElasticSearchPublisher(config)

        return None

    def get_producer(self):
        return eV.EventadorProducer(self.config['brokers'], self.config['topic'])

