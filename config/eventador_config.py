config = {
    "brokers": '',  # Eventador plain text broker
    "topic": 'tweets',   # Eventador (Kafka Topics)
    "max_records": 10,   # max records to stream from twitter
}

# S3 Config
def add_publisher_config(common, config):
    c = common.copy()
    c.update(config)
    return c


s3_config = add_publisher_config(config, {
    "publisher": "s3",
    "bucket": "testdiscursive",  # S3 Bucket
})


# Elasticsearch Config
es_config = add_publisher_config(config, {
    "publisher": "es",
    "index": "twitter",
    "doc_type": "tweets"
})
