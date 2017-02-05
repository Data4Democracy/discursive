from config import esconn

# get Elasticsearch connection
es = esconn.esconn()


def getStreamResultHandles():
    resp = es.search(index="twitter", doc_type="tweets", size="100", filter_path=['hits.hits._source.name'])
    output = set()
    for doc in resp['hits']['hits']:
        output.add(doc['_source']['name'])
    return list(output)


def getStreamResultStatusIDs(size):
    resp = es.search(index="twitter", doc_type="tweets", size=size, filter_path=['hits.hits._source.id_str'])
    output = set()
    for doc in resp['hits']['hits']:
        output.add(doc['_source']['id_str'])
    return list(output)

