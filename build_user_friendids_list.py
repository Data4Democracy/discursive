import time
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
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3, retry_delay=60)

# load Twitter handle(s) & build a search for friends
screen_name_list = getStreamResultHandles()

def getFriendsbyHandle(handles):
    for handle in screen_name_list:
        ids = []
        page_count = 0
        for page in tweepy.Cursor(api.friends_ids, screen_name=handle, count=5000).pages():
            page_count += 1
            print 'Getting page {} for followers ids'.format(page_count)
            ids.extend(page)
        return ids

# print for review
for x in screen_name_list:
    print (getFriendsbyHandle(screen_name_list))

