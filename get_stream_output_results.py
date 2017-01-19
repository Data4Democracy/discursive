import json
from elasticsearch import Elasticsearch, helpers
from config import esconn

# get Elasticsearch connection
es = esconn.esconn()

def getStreamResultHandles():
    resp = es.search(index="twitter", doc_type="message", size="100", filter_path=['hits.hits._source.name'])
    output = set()
    for doc in resp['hits']['hits']:
        output.add(doc['_source']['name'])
    return list(output)

def getStreamResultStatusIDs():
    resp = es.search(index="twitter", doc_type="message", size="1", filter_path=['hits.hits._source.id_str'])
    output = set()
    for doc in resp['hits']['hits']:
        output.add(doc['_source']['id_str'])
    return list(output)

# write output to file
#with open('stream_output_handles.txt', 'w') as f:
#    f.write(str(getStreamResultHandles())
#print list(getStreamResultStatusIDs())

