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
            print status.text.encode('utf8') + ' ' + handle

def getUserInfobyHandle(handles):
    for handle in handles:
        user_info = {handle: []}
        try:
            user = api.get_user(handle, include_entities=1)
            user_info[handle].append(
                {'active': 'True',
                'bio': user.description,
                'location': user.location,
                'followers': user.followers_count,
                'following': user.friends_count,
                'image': user.profile_image_url,
                })
        except:
            user_info[handle].append(
                {'active': 'False',
                'bio': 'none',
                'location': 'none',
                'followers': 'none',
                'following': 'none',
                'image': 'none',

                })
        yield user_info


# print for review
#for handle in screen_name_list:
#    print getTweetsbyHandle(json.dumps(screen_name_list))

users_info = getUserInfobyHandle(screen_name_list)
print users_info.next()
with open('user_info.json', 'w') as fp:
    for user_info in users_info:
        json.dump(user_info, fp, indent=1)