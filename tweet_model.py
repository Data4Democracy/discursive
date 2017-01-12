def map_tweet_for_es(tweet, topics, extra=None):
    tweet_dict = {
        'name': tweet.user.screen_name,
        'message': tweet.text,
        'description': tweet.user.description,
        'loc': tweet.user.location,
        'text': tweet.text,
        'user_created': tweet.user.created_at,
        'followers': tweet.user.followers_count,
        'id_str': tweet.id_str,
        'created': tweet.created_at,
        'retweet_count': tweet.retweet_count,
        'friends_count': tweet.user.friends_count,
        'topics': topics
    }

    if extra is not None:
        final = tweet_dict.copy()
        final.update(extra)
        return final
    else:
        return tweet_dict
