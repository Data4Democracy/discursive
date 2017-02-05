from datetime import datetime as dt
from config import s3conn
import json
import os, sys


def parse_args_for_topics():
    if len(sys.argv) > 2:
        sys.exit('ERROR: Received 2 or more arguments: {} {} {} Expected 1: Topic file name'
                 .format(sys.argv[0], sys.argv[1], sys.argv[2]))

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
        except Exception as ex:
            sys.exit('ERROR: Default topics.txt not found. No alternate topic file  was provided')

    return [topic.replace('\n', '').strip() for topic in topics]


def dump_to_elastic(es, bodydata):
    es.index(index='twitter', doc_type="message", body=bodydata)


def dump_to_s3(data):
    filename, ext = ("tweets", ".json")

    local_file = dump_to_file(data, filename + ext)
    tweets_file = open(local_file, 'rb')

    key = create_key()
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
        print(str(ex))


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


def create_key():
    filename, ext = ("tweets", ".json")
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