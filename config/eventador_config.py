brokers = ''

s3config = {
    "brokers": brokers, # Eventador plain text broker
    "topic": 'tweets',  # Eventador (Kafka Topics)
    "bucket": 'testdiscursive', # S3 Bucket
    "max_records": 10, # max records to stream from twitter
    "publisher": 's3'  # some kind of backend publisher i.e. s3, elasticsearch, etc
}
