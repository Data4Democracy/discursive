from __future__ import print_function
import sys
import tweepy
from elasticsearch import helpers
from config import esconn, twitter_config
from tweet_model import map_tweet_for_es

reload(sys)
sys.setdefaultencoding('utf8')

# go get elasticsearch connection
es = esconn.esconn()

# auth & api handlers
auth = tweepy.OAuthHandler(twitter_config.CONSUMER_KEY, twitter_config.CONSUMER_SECRET)
auth.set_access_token(twitter_config.ACCESS_TOKEN, twitter_config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# load topics & build a search
topics = ["oath keeper"]
search = api.search(q=topics, count=100)


# function for screen_name, text, search topic
def tweet_text():
    for tweet in search:
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
            yield map_tweet_for_es(tweet, topics)

# bulk insert into twitter index
helpers.bulk(es, tweet_text(), index='twitter', doc_type='tweets')

# view the message field in the twitter index
messages = es.search(index="twitter", size=1000, _source=['message'])
print(messages)

