from __future__ import print_function

import sys

import index_twitter_utils as utils
import twitter_api_setup as api_setup
from config import eventador_config
from eventador import eventador_client
from eventador import eventador_utils as eu
from tweet_model import map_tweet_for_es

import json

reload(sys)
sys.setdefaultencoding('utf8')

def tweet_text(topics, count, producer, key):
    search = api_setup.api.search(q=topics, count=count)

    def gen_search(counter = 0):
        for tweet in search:
            if (not tweet.retweeted) and ('RT @' not in tweet.text):
                counter += 1
                mapped_tweet = map_tweet_for_es(tweet, topics)
                print('Tweet Count# ' + str(counter) + ' ' + json.dumps(utils.fix_date_for_tweet(mapped_tweet)))
                yield mapped_tweet

    producer.send_all(key, gen_search())


def do_twitter_search():
    count = 1000
    topics = ["oath keeper"]

    eventador_config.config['max_records'] = 20
    client = eventador_client.EventadorClient(eventador_config.config)
    producer = client.get_producer()
    key = topics[0]

    es_publisher = eu.start_publishers(client, [eventador_config.es_config()], [key])
    tweet_text(topics, count, producer, key)
    eu.wait_for_publishers(es_publisher)


do_twitter_search()


