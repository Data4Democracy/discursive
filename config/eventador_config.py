brokers = ''

s3config = {
    "brokers": brokers,
    "topic": 'tweets',
    "bucket": 'testdiscursive',
    "max_records": 10,
    "publisher": 's3'  # some kind of backend publisher i.e. s3, elasticsearch, etc
}
