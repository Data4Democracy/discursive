from __future__ import print_function
from config import esconn

# get Elasticsearch connection
es = esconn.esconn()

def getStreamResultHandles():
    resp = es.search(index="twitter", doc_type="message", size="100", filter_path=['hits.hits._source.name'])
    output = set()
    for doc in resp['hits']['hits']:
        output.add(doc['_source']['name'])
    return list(output)


print(list(getStreamResultHandles()))
