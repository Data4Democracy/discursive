from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import aws_config

host = aws_config.es_host
awsauth = AWS4Auth(aws_config.access_id, aws_config.access_secret, 'us-west-2', 'es')


def esconn():
    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    return es
