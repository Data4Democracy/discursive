import json
import tweepy
from config import esconn, aws_config, twitter_config
from elasticsearch import Elasticsearch,helpers
from get_stream_output_handles import getStreamResultHandles

# unicode mgmt
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# go get elasticsearch connection
es = esconn.esconn()

# auth & api handlers
auth = tweepy.OAuthHandler(twitter_config.CONSUMER_KEY, twitter_config.CONSUMER_SECRET)
auth.set_access_token(twitter_config.ACCESS_TOKEN, twitter_config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# load Twitter handle(s) & build a search for followers
screen_name_list = getStreamResultHandles()

def getTweetsbyHandle(handles):
    for handle in screen_name_list:
        search = api.user_timeline(screen_name=handle, count=200, include_rts=True)
        for status in search:
            print status.text + ' ' + handle

# print for review
for handle in screen_name_list:
    print getTweetsbyHandle(json.dumps(screen_name_list))

