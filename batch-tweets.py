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

for item in search:
  for tweet in tweepy.Cursor(api.search,q=search,count=1000,
                           lang="en",
                           since="2018-08-27").items():
    model = falcon.model_tweet(json.loads(tweet._json), [search])
    if model is not None:
      dobbins.insert_entry(model)
