# Twitter API token/keys
import os

ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""

# AWS Config
# or your settings here
access_id = os.environ["AWS_ACCESS_KEY_ID"]
access_secret = os.environ["AWS_SECRET_ACCESS_KEY"]
s3_endpoint_url = ""
es_host = ''


#MONGO
mongo_config = {
    'host': '',
    'db': '',
    'port': '',
    'user': '',
    'password':''
}
