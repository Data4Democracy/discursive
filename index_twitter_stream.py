from __future__ import print_function
import json
import sys
import threading
import tweepy
import index_twitter_utils as utils
import twitter_auth_setup as tas
from tweet_model import map_tweet_for_es
from config import eventador_config
from eventador import eventadorClient as ec
from config import esconn

reload(sys)
sys.setdefaultencoding('utf8')

class StreamListener(tweepy.StreamListener):
    def __init__(self, config, api=None):
        super(StreamListener, self).__init__()
        self.config = config
        self.counter = 0
        self.limit = self.config['max_records']
        self.tweet_list = []

    def on_status(self, status):
        if self.counter < self.limit:
            extra = utils.create_extra_fields(status)
            tweet = map_tweet_for_es(status, self.config['twitter_topics'], extra)

            # append to instance attribute and then index to elasticsearch (rethink if limit scales up significantly)
            self.tweet_list.append(tweet)
            utils.dump_to_elastic(self.config['es'], tweet)

            print('Tweet Count# ' + str(self.counter) + ' ' + json.dumps(utils.fix_date_for_tweet(tweet)))
        else:
            self.config['producer'].send_all(self.config['file_key'], utils.fix_dates_for_dump(self.tweet_list))
            return False

        self.counter += 1

    def on_error(self, status_code):
        # Twitter is rate limiting, exit
        if status_code == 420:
            print('Twitter rate limit error_code {}, exiting...'.format(status_code))
            return False

def invoke_stream_listener(config):
    stream_listener = StreamListener(config)
    stream = tweepy.Stream(auth=tas.api.auth, listener=stream_listener)
    stream.filter(track=config['twitter_topics'])

def start_eventador(target, target_args, callback, c_args):
    thread = threading.Thread(target=target, args=target_args)
    thread.start()
    callback(c_args)
    return thread

def do_twitter_stream(get=10):
    # Get Eventador Client
    client = ec.EventadorClient(eventador_config.s3config)

    # Get Attributes
    producer, publisher = client.get_producer_and_publisher()
    twitter_topics = utils.parse_args_for_topics()
    file_key = utils.create_key()
    es = esconn.esconn()

    config = {
        'es': es,
        'file_key': file_key,
        'twitter_topics': twitter_topics,
        'producer': producer,
        'max_records': get
    }

    eventador = start_eventador(publisher.publish, [file_key], callback=invoke_stream_listener, c_args=config)
    eventador.join()

do_twitter_stream()
