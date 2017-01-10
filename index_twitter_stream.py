import json
import tweepy
import config
import os
from esconn import esconn
import s3conn
from datetime import datetime as dt

# unicode mgmt
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# Twitter auth and api call setup
auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Get elasticsearch connection
es = esconn()

if len(sys.argv) >= 2:
    sys.exit('ERROR: Received 2 or more arguments. Expected 1: Topic file name')

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
        else:
            # if limit reached write saved tweets to s3
            dump_to_s3(self.tweet_list)
            return False

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
                'description': description,
                'loc': loc,
                'text': text,
                'name': name,
                'user_created': user_created,
                'followers': followers,
                'id_str': id_str,
                'created': created,
                'retweet_count': retweet_count,
                'friends_count': friends_count,
                'retweet': retweet,
                'original_id': original_id,
                'original_name': original_name,
                'hashtags': hashtags
                }

        # append to instance attribute and then index to elasticsearch (rethink if limit scales up significantly)
        self.tweet_list.append(tweet)
        dump_to_elastic(tweet)

        self.counter += 1
        print 'Tweet Count# ' + str(self.counter) + ' ' + str(text)

    def on_error(self, status_code):
        # Twitter is rate limiting, exit
        if status_code == 420:
            print('Twitter rate limit error_code {}, exiting...'.format(status_code))
            return False


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
    tweet_list = json.dumps(fix_dates_for_serialization(data))

    # get current working directory and write file to local path
    cwd = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(cwd, filename)
    try:
        with open(path, 'w') as fw:
            fw.write(tweet_list)
        return path
    except (IOError, OSError) as ex:
        print str(ex)


def fix_dates_for_serialization(data):
    # json.dumps can't natively serialize datetime obj converting to str before
    for tweet in data:
        tweet["user_created"] = str(tweet["user_created"])
        tweet["created"] = str(tweet["created"])
    return data


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
