import json
import tweepy
from config import esconn, aws_config, twitter_config
import os
from datetime import datetime as dt
from tweet_model import map_tweet_for_es
from config import s3conn

# unicode mgmt
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# Twitter auth and api call setup
auth = tweepy.OAuthHandler(twitter_config.CONSUMER_KEY, twitter_config.CONSUMER_SECRET)
auth.set_access_token(twitter_config.ACCESS_TOKEN, twitter_config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Get elasticsearch connection
es = esconn.esconn()

if len(sys.argv) > 2:
    sys.exit('ERROR: Received 2 or more arguments: {} {} {} Expected 1: Topic file name'.format(sys.argv[0], sys.argv[1], sys.argv[2]))

elif len(sys.argv) == 2:
    try:
        with open(sys.argv[1]) as f:
            topics = f.readlines()
    except Exception:
        sys.exit('ERROR: Expected topic file %s not found' % sys.argv[1])
else:
    try:
        with open('topics.txt') as f:
            topics = f.readlines()
    except:
        sys.exit('ERROR: Default topics.txt not found. No alternate topic file  was provided')


TOPICS = [topic.replace('\n', '').strip() for topic in topics]


class StreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        super(StreamListener, self).__init__()
        self.counter = 0
        self.limit = 500
        self.tweet_list = []

    def on_status(self, status):
        if self.counter < self.limit:
            extra = create_extra_fields(status)
            tweet = map_tweet_for_es(status, TOPICS, extra)

            # append to instance attribute and then index to elasticsearch (rethink if limit scales up significantly)
            self.tweet_list.append(tweet)
            dump_to_elastic(tweet)

            print 'Tweet Count# ' + str(self.counter) + ' ' + json.dumps(fix_date_for_tweet(tweet))
        else:
            # if limit reached write saved tweets to s3
            dump_to_s3(self.tweet_list)
            return False

        self.counter += 1

    def on_error(self, status_code):
        # Twitter is rate limiting, exit
        if status_code == 420:
            print('Twitter rate limit error_code {}, exiting...'.format(status_code))
            return False


def create_extra_fields(status):
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

    return {
        'retweet': retweet,
        'hashtags': hashtags,
        'original_id': original_id,
        'original_name': original_name
    }


def search():
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=TOPICS)
    return


def dump_to_elastic(bodydata):
    es.index(index='twitter', doc_type="message", body=bodydata)


def dump_to_s3(data):
    filename, ext = ("tweets", ".json")

    local_file = dump_to_file(data, filename + ext)
    tweets_file = open(local_file, 'rb')

    key = create_key(filename, ext)
    s3conn.write_file_to_s3(tweets_file, key)


def dump_to_file(data, filename):
    # fix dates and dump to json
    tweet_list = json.dumps(fix_dates_for_dump(data))

    # get current working directory and write file to local path
    cwd = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(cwd, filename)
    try:
        with open(path, 'w') as fw:
            fw.write(tweet_list)
        return path
    except (IOError, OSError) as ex:
        print str(ex)


def fix_dates_for_dump(data):
    # json.dumps can't natively serialize datetime obj converting to str before
    for tweet in data:
        tweet["user_created"] = str(tweet["user_created"])
        tweet["created"] = str(tweet["created"])
    return data

def fix_date_for_tweet(tweet):
    tweet["user_created"] = str(tweet["user_created"])
    tweet["created"] = str(tweet["created"])
    return tweet


def create_key(filename, ext):
    now = dt.now()
    # Ex: '2017/1/9/21/tweets-26.json'
    # This key generates a 'directory' structure in s3 that can be navigated as such
    key = str(now.year) + "/" + \
        str(now.month) + "/" + \
        str(now.day) + "/" + \
        str(now.hour) + "/" + \
        filename + "-" + \
        str(now.minute) + ext
    return key


search()
