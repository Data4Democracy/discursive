# discursive

This tool searches Twitter for a given topic and stores the status, user and search topic in an Elasticsearch index.The intended use case is for social network composition and Tweet text analysis. 

Sooner-than-later this work should be merged with [@bstarling's fantastic work](https://github.com/bstarling/twitter-framework) as a one-stop-shop for search/streaming. And, we have a nifty new backend/supporting infrastructure on the roadmap courtesy of [@nataliaking](https://github.com/nataliaking)! Therefore, **please do consider this a temporary bridge to a better place**, but useful in the meantime if you want to source domains for [scrape-right](https://github.com/Data4Democracy/scrape-right) tasking or start to build out lists of Twitter handles. 

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

Once everything is installed and you're ready to rock:

1. Insert your desired keyword in the `index_twitter_search.py` file in this part: 

```python
# load topics & build a search
topics = ["oath keeper"]
search = api.search(q=topics, count=100)
```
Currently, you can only search for one thing at a time because, well, I haven't gotten around to building a list of search terms and fancy stuff like that. I suspect that'll likely come as a component of a larger refactoring during the merge of @bstarling's work and @nataliaking's supporting infrastructure design. But, if someone wants to bite that off now, feel free to PR it!

2. Setup your AWS and Twitter configs

   - Go into `config.py` and drop in your Twitter token/keys
   - Go into `esconn.py` and drop in your AWS Elasticsearch domain host and AWS auth

3. Run `essetup.py` which'll generate the index with the appropriate mappings and whatnot

4. Curse me for doing this in Python 2.7

   - There are reasons. Just none that I want to admit to here. A move to 3x will come soon I'm sure.

## Fire for effect

Once you're done configuring everything from above run `python index_twitter_search_py` which will, the first time you run it (error free, of course), tell you there are no documents. Subsequent runs spit out a bunch of text to your console that you can turn off by commenting out this unsightly thing:

``` python
# view the message field in the twitter index
messages = es.search(index="twitter", size=1000, _source=['message'])
print messages
```
As one may imagine, running this does a bulk insert of Tweets you searched for into Elasticsearch (the user, tweet text and search topic). You can then use Kibana if you like or just `curl` out to your fancy new Elasticsearch index to do all the wonderful Elasticsearch-y things. To be sure, you could also use [Postman](https://www.getpostman.com/) or some other browser-based tooling like a sane person.

## Where to find help

There is a chance setting all this up gives you problems. How great a chance? I don't care to speculate publically. I'm @nick on our Slack or you can file an issue here (please for my sanity just join us on Slack and let's talk there).

## Want to use my infra?

I am a-ok with sharing access to the running instance of Kibana on a per-IP basis until we get new infra up. I am even happy to take your search term requests and type them into my functioning configuration of this thing and have them indexed if you want to send them to me. I will do this for free because we're fam. 

## Roadmap

We have no formal roadmap yet, other than to say a new supporting infra is forthcoming and we are going to finish building a search/stream Twitter capability. That said, here's some suggested stuff until we get a community roadmap: 

- Help do the merge of stream/search capability referenced throughout this doc
- Ensure we have functions capable of returning all the important parts of a Tweet/profile (follower counts, RTs, domains, etc.)
- Begin working on an NLP capability (I personally heart Spacy) to get some basics carved out of the Tweet statuses (entities, POS, etc.)
- Anything else we want to do as a community!
