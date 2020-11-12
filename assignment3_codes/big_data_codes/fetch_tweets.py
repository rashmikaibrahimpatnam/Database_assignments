import tweepy
from listener import TweeListener
from tweepy import Stream
from connect_db import ConnectDb
from clean_data import CleanData
import bson

'''
class that extracts tweets using the 
streaming in tweepy
'''

class TweetExtraction():
    def __init__(self,connect):
        self.connect = connect

    def consumer_keys(self):
        #consumer keys to access the twitter data
        consumer_data = {
            'consumer_key' : 'rYFc53eLpNJbaYzU8EVNhfwiu',
            'consumer_token' : 'tNajj6kV5s4lUNDBbx1fsyfgyppsulvdkrJ3mNtCqOVZ5vgKUS'
        }
        return consumer_data
    
    def access_keys(self):
        #access keys to access the twitter data
        access_data = {
            'access_key' : '1318181986637406210-IE75qR0OTC9DZYwx6AMsty5mZSDPKv',
            'access_token' : '5mckhalaxJe7GN6UGIAlKDrD8pFedE6lwve7B84S578iN'
        }
        return access_data

    def set_auth(self):
        #function to set up the authorization 
        consumer = self.consumer_keys()
        access = self.access_keys()
        authorize = tweepy.OAuthHandler(consumer['consumer_key'],consumer['consumer_token'])
        authorize.set_access_token(access['access_key'],access['access_token'])
        return authorize
    
    def stream_data(self,keywords):
        #function that calls the Stream from tweepy for fetching the tweets
        tweelistener = TweeListener(self.connect)
        authcred = self.set_auth()
        stream = Stream(auth=authcred,listener=tweelistener)
        stream.filter(track=keywords)

    def process_data(self):
        #function that cleans the fetched tweets and inserts into processdb
        data = ConnectDb().find_data(self.connect,'RawDb','RawTweets')
        for value in data:
            processed_data = {}
            for prop in value:

                if (isinstance(value[prop],bson.objectid.ObjectId)) | (value[prop] == None):
                    if value[prop] == None:
                        processed_data[prop] = value[prop]
                else: 
                    formatted = CleanData().clean_emoji_data(value[prop]) #remove emoji
                    clean_url = CleanData().clean_url_data(formatted) #remove url
                    clean_spc = CleanData().clean_spc_chars(clean_url) #remove special characters
                    processed_data[prop] = clean_spc
            #insert cleaned data into process db
            ConnectDb().insert_data(processed_data,self.connect,'ProcessDb','Tweets')

if __name__ == "__main__":
    
    conn_db = ConnectDb()
    conn = conn_db.connect_mongo() 
    tweet_extract = TweetExtraction(conn)
    tweet_extract.stream_data(['Storm', 'Winter', 'Canada', 'Temperature', 'Flu', 'Snow', 'Indoor', 'Safety'])
    tweet_extract.process_data()
    conn.close()
    
