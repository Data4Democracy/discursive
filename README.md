# discursive

This tool searches Twitter for a collection of topics and stores the Tweet data in an Elasticsearch index _and_ an S3 bucket. The intended use case is for social network composition and Tweet text analysis. 

## Setup

Everything you see here runs on AWS EC2 and the AWS Elasticsearch service. Currently, it runs just fine in the free tier. Things you will need include:

- An AWS account
- An [AWS Elasticsearch domain](http://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-gsg.html)
- To [configure an access policy for Kibana](https://aws.amazon.com/blogs/security/how-to-control-access-to-your-amazon-elasticsearch-service-domain/) if you want to use that
- An EC2 Linux image (this was tested on Ubuntu)
- A Twitter account and associated [application](https://apps.twitter.com/) auth keys/tokens
- Some grit and [determination](http://www.memecenter.com/fun/333919/determination)

This sounds like a lot, but was quite quick to cobble together.

## Scouring the Twitterverse

Once you have cloned the repo you're ready to rock:

1. Install Docker on your EC2 instance using [instructions appropriate for your OS](https://docs.docker.com/engine/getstarted/step_one/#/docker-for-linux) (the code in this repo is run using Ubuntu).

2. Change into the Discursive directory (i.e. `cd discursive/`).

3. Run `essetup.py` which is located in the `/config` directory, which'll generate the Elasticsearch index with the appropriate mappings.

4. Update the `aws_config.py` `twitter_config.py` `esconn.py` and `s3conn.py` files located in the `/config` directory with your credentials.

5. Put your desired keyword(s) in the `topics.txt` file (one term per line).

6. Edit the `crontab` file to run at your desired intervals. The default will run every fifteen minutes. 

7. Run `sudo docker build -t discursive .`

8. Run `sudo docker run discursive`

9. If all went well you're watching Tweets stream into your Elasticsearch index! Conversely, run `index_twitter_search.py` to search for specific topic(s) and bulk insert the data into your Elasticsearch index (and see the messages from Elasticsearch returned to your console).

10. There are several options you may want to configure/tweak. For instance, you may want to turn off printing to console (which you can do in `index_twitter_search.py`) or run the container as a detached process. Please do jump into our Slack channel #assemble if you have any questions or log an issue!

## Explore Twitter networks

A warning, **this is experimental** so check back often for updates. There are four important files for exploring the network of Tweets we've collected:

* `get_stream_output_results.py` - returns distinct handles (usernames in Twitter) and Tweet IDs (statuses in Twitter) from the Elasticsearch index for a specified number of Tweets 
* `build_user_followers_list.py` - taking the result from `get_stream_output_results.py` it returns a list of followers for each input handle
* `build_user_friendids_list.py` - taking the result from `get_stream_output_results.py` it returns a list of friends for each input handle
* `build_user_timelines_list.py` - taking the result from `get_stream_output_results.py` it returns a list of tweets for each input handle
* `build_status_attr.py` - taking the result from `get_stream_output_results.py` it returns the full Tweet object (see Twitter API doc for details)

So, with some additional munging, you can use the above to build a graph of users, their followers and friends. When combined with the additional data we collect (tweet text, retweets, followers count, etc.) this represents the beginning of our effort to enable analysts by providing curated, network-analysis-ready data! 

## Where to find help

There is a chance setting all this up gives you problems. How great a chance? I don't care to speculate publically. I'm @nick on our Slack or you can file an issue here (please for my sanity just join us on Slack and let's talk there).

## Want to use our infra?

I am a-ok with sharing access to the running instance of Elasticsearch until we get new infra up. I am even happy to take your search term requests and type them into my functioning configuration of this thing and have them indexed if you want to send them to me. I will do this for free because we're fam. Just ping me. 

## Current Work & Roadmap

- Migrate the data collection components of this project to [assemble](https://github.com/Data4Democracy/assemble). This includes the underlying
infrastructure and associated codebase. This repo will then become home to curated Twitter datasets and analytical products (contact @bstarling, @asragab or @natalia on the #assemble channel on Slack)
    - https://github.com/Data4Democracy/discursive/issues/11
    - https://github.com/Data4Democracy/discursive/issues/13
    - https://github.com/Data4Democracy/discursive/issues/14
    - https://github.com/Data4Democracy/discursive/issues/15
- Design, develop and maintain a robust Natural Language Processing (NLP) capability for Twitter data (contact @divya or @wwymak on the #nlp-twitter channel on Slack)
    - https://github.com/Data4Democracy/discursive/issues/17
- Design, develop and maintain a community detection and network analysis capability for Twitter data (contact @alarcj or @zac_bohon on the #discursive-commdetect channel on Slack)
    - https://github.com/Data4Democracy/discursive/issues/4

## Working with Docker

- Once you have Docker up and running, here are a few useful commands:
    ```
    # build the image
    sudo docker build -t discursive .

    # list all images
    sudo docker images -a

    # if you need to remove the image
    sudo docker rmi -f 4f0d819f7a47

    # run the container for reals; prints a bunch of junk
    sudo docker run -it -v $HOME/.aws:/home/aws/.aws discursive python /discursive/index_twitter_stream.py
    ```
