from __future__ import print_function
import json
import sys

import tweepy
import index_twitter_utils as utils
import twitter_api_setup as api_setup
from tweet_model import map_tweet_for_es
from config import eventador_config
from eventador import eventador_client as ec
from eventador import eventador_utils as eu


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
            self.tweet_list.append(tweet)
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


def do_twitter_stream(get=10):
    # Get Eventador Client
    eventador_config.config['max_records'] = get
    client = ec.EventadorClient(eventador_config.config)

    # Create config object for Stream Listener
    listener_config = {
        'file_key': utils.create_key(),
        'twitter_topics': utils.parse_args_for_topics(),
        'producer': client.get_producer(),
        'max_records': get
    }

    # add config for each kind of publisher available
    publishers = eu.start_publishers(client,
                                  publisher_configs=[eventador_config.es_config()],
                                  publish_args=[listener_config['file_key']])

    invoke_stream_listener(listener_config)
    eu.wait_for_publishers(publishers)  # Wait for eventador threads to finish


def invoke_stream_listener(config):
    stream_listener = StreamListener(config)
    stream = tweepy.Stream(auth=api_setup.api.auth, listener=stream_listener)
    stream.filter(track=config['twitter_topics'])


do_twitter_stream()
