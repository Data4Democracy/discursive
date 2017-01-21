import tweepy
from config import esconn, twitter_config
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


def getAttributesbyStatusID(statuses):
        search = api.statuses_lookup(statuses, include_entities='yes')
        for item in search:
            # print str(item.id) + ': ' + item.text
            yield item

# load Twitter screen_name & build a search
status_id_list = getStreamResultStatusIDs(size=10)
output = {item for item in getAttributesbyStatusID(status_id_list)}

print output
