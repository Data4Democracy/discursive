from __future__ import print_function
import sys
import tweepy
from config import esconn, twitter_config
from get_stream_output_handles import getStreamResultHandles

reload(sys)
sys.setdefaultencoding('utf8')

# go get elasticsearch connection
es = esconn.esconn()

# auth & api handlers
auth = tweepy.OAuthHandler(twitter_config.CONSUMER_KEY, twitter_config.CONSUMER_SECRET)
auth.set_access_token(twitter_config.ACCESS_TOKEN, twitter_config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# load Twitter screen_name & build a search

#search = api.user_timeline('hadoopjax', count=2)
#screen_name_list = ['hadoopjax']
screen_name_list = getStreamResultHandles()

def getFollowersbyHandle(handles):
    for handle in screen_name_list:
        search = tweepy.Cursor(api.followers, screen_name=handle, count=200).items()
        for user in search:
            print(user.screen_name)


output = set()
for handle in screen_name_list:
    output.add(getFollowersbyHandle(screen_name_list))

print(output)
