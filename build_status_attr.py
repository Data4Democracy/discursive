import tweepy
from config import esconn, aws_config, twitter_config
from elasticsearch import Elasticsearch,helpers
from get_stream_output_results import getStreamResultStatusIDs

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

# load Twitter screen_name & build a search

#search = api.user_timeline('hadoopjax', count=2)
#screen_name_list = ['hadoopjax']
status_id_list = getStreamResultStatusIDs()

search = api.statuses_lookup('813859926485463040')
        for item in search:
            print item.id + ' ' + item.text

#output = set()
#for status in status_id_list:
#    output.add(getAttributesbyStatusID(status_id_list))

print getAttributesbyStatusID()

