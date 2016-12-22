from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

# go get elasticsearch connection
from esconn import esconn
es = esconn()

# use this to delete an index
if es.indices.exists(index='twitter'):
    es.indices.delete(index='twitter')

# use this to create an index
settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "tweets": {
            "properties": {
                "message": {"type": "string"},
                "user": {"type": "string", "store": "true"},
                "topic": {"type": "string"}
            }
        }
     }
}
es.indices.create(index='twitter', body=settings)

# check if the index now exists
if es.indices.exists(index='twitter'):
    print 'Created the index'
else:
    print 'Something went wrong. The index was not created.'
