import json
import tweepy
import config
from elasticsearch import Elasticsearch,helpers

# unicode mgmt
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# Twitter auth and api call setup
auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Get elasticsearch connection
from esconn import esconn
es = esconn()

# Update with topics to follow
if sys.argv[1]:
    f = open(sys.argv[1])
else:
    f = open('topics.txt')
    
topics = f.readlines()
TOPICS = [topic.replace('\n', '').strip() for topic in topics]


class StreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        super(StreamListener, self).__init__()
        self.counter = 0
        self.limit = 500

    def on_status(self, status):
        if self.counter < self.limit:
            description = status.user.description
            loc = status.user.location
            text = status.text
            name = status.user.screen_name
            user_created = status.user.created_at
            followers = status.user.followers_count
            id_str = status.id_str
            created = status.created_at
            retweet_count = status.retweet_count
            friends_count = status.user.friends_count

        # check if retweet, assign attributes
        if hasattr(status, 'retweeted_status'):
            retweet = 'Y'
            original_id = status.retweeted_status.user.id
            original_name = status.retweeted_status.user.name
        else:
            retweet = 'N'
            original_id = None
            original_name = None

        # check for hashtags and save as list
        if hasattr(status, 'entities'):
            hashtags = []
            for tag in status.entities['hashtags']:
                hashtags.append(tag['text'])
            hashtags = json.dumps(hashtags)

        # Elasticsearch document mapping setup
        tweet = {
                'description':description,
                'loc':loc,
                'text':text,
                'name':name,
                'user_created':user_created,
                'followers':followers,
                'id_str':id_str,
                'created':created,
                'retweet_count':retweet_count,
                'friends_count':friends_count,
                'retweet':retweet,
                'original_id':original_id,
                'original_name':original_name,
                'hashtags':hashtags
                }
        dumpToElastic(tweet)
        self.counter += 1
        print 'Tweet Count# ' + `self.counter` + ' ' + str(description)

    def on_error(self, status_code):
        '''Twitter is rate limiting, exit'''

        if status_code == 420:
            print('Twitter rate limit error_code {}, exiting...'.format(status_code))
            return False

def search():
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=TOPICS)

def dumpToElastic(bodydata):
    es.index(index='twitter', doc_type="message", body=bodydata)

search()
