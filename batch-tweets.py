from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import tweepy
import csv

import configparser

config = configparser.ConfigParser()
config.read('config.ini')
import sys
sys.path.append(config['twits']['twits_path'])

from twits.es import ESClient
from twits.modeller import Modeller

import json

falcon = Modeller()
dobbins = ESClient()

consumer_key = config['twits']['consumer_key']
consumer_secret = config['twits']['consumer_secret']
access_token = config['twits']['access_token']
access_secret = config['twits']['access_secret']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)

csvFile = open('ua.csv', 'a')
csvWriter = csv.writer(csvFile)

search = config['twits']['search'].split(',')

search = ['hello']

from datetime import datetime

dt_obj = datetime.strptime('20.12.2016 09:38:42,76',
                           '%d.%m.%Y %H:%M:%S,%f')
millisec = dt_obj.timestamp() * 1000

print(millisec)

def timestamp(self):
        "Return POSIX timestamp as float"
        if self._tzinfo is None:
            s = self._mktime()
            return s + self.microsecond / 1e6
        else:
            return (self - _EPOCH).total_seconds()

for item in search:
  for tweet in tweepy.Cursor(api.search,q=item,count=1000,
                           lang="en",
                           since="2018-08-27").items():
    tweet_info = tweet._json.copy()
    tweet_info['timestamp_ms'] = timestamp(datetime.strptime(tweet_info['created_at'],'%a %b %m %X %z %Y')) * 1000
    model = falcon.model_tweet(json.loads(tweet._json), [search])
    if model is not None:
      dobbins.insert_entry(model)
