# go get elasticsearch connection
from esconn import esconn

es = esconn()

# use this to delete an index
if es.indices.exists(index='twitter'):
    es.indices.delete(index='twitter')

# use this to create an index
settings = {
    'settings': {
        'number_of_shards': 1,
        'number_of_replicas': 0
    },
    'mappings': {
        'tweets': {
            'properties': {
                'name': {'type': 'string'},
                'message': {'type': 'string'},
                'description': {'type': 'string'},
                'loc': {'type': 'string'},
                'text': {'type': 'string', 'store': 'true'},
                'user_created': {'type': 'date'},
                'followers': {'type': 'long'},
                'id_str': {'type': 'string'},
                'created': {'type': 'date', 'store': 'true'},
                'retweet_count': {'type': 'long'},
                'friends_count': {'type': 'long'},

                # These fields are synthesized from other metadata
                'topics': {'type': 'string', 'store': 'true'},
                'retweet': {'type': 'string'},
                'hashtags': {'type': 'string', 'store': 'true'},
                'original_id': {'type': 'string'},
                'original_name': {'type': 'string'}
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
