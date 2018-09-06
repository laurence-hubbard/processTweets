from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
import sys

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

sys.path.append(config['twits']['twits_path'])

from twits.es import ESClient
from twits.modeller import Modeller
import json

consumer_key = config['twits']['consumer_key']
consumer_secret = config['twits']['consumer_secret']
access_token = config['twits']['access_token']
access_secret = config['twits']['access_secret']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

falcon = Modeller()
dobbins = ESClient()

search = config['twits']['search'].split(',')

class MyListener(StreamListener):

    def on_data(self, data):
        try:
            model = falcon.model_tweet(json.loads(data), search)
            if model is not None:
                dobbins.insert_entry(model)
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=search)
