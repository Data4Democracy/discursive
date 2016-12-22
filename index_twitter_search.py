import tweepy
import config
from elasticsearch import Elasticsearch,helpers

# unicode mgmt
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# go get elasticsearch connection
from esconn import esconn
es = esconn()

# auth & api handlers
auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# load topics & build a search
topics = ["oath keeper"]
search = api.search(q=topics, count=100)

# function for screen_name, text, search topic
def tweet_text():
    for tweet in search:
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
            yield {
                    'name': tweet.user.screen_name,
                    'message': tweet.text,
                    'search_topic': topics,
                    'description':tweet.user.description,
                    'loc':tweet.user.location,
                    'text':tweet.text,
                    'user_created':tweet.user.created_at,
                    'followers':tweet.user.followers_count,
                    'id_str':tweet.id_str,
                    'created':tweet.created_at,
                    'retweet_count':tweet.retweet_count,
                    'friends_count':tweet.user.friends_count
                  }

# bulk insert into twitter index
helpers.bulk(es, tweet_text(), index='twitter', doc_type='message')

# view the message field in the twitter index
messages = es.search(index="twitter", size=1000, _source=['message'])
print messages
