from tweepy import StreamListener
import json
from connect_db import ConnectDb

'''
Listener class that fetches the tweets for the 
given keywords
'''
class TweeListener(StreamListener):
    def __init__(self,connection):
        self.tweet_limit = 1000 #limit on fetching the tweets
        self.count = 0
        self.connection = connection

    def on_data(self, raw_data):
        '''
        Function that fetches the tweets based on the keyword and
        inserts the required data into the database
        '''
        self.count += 1
        if(self.tweet_limit < self.count):
            return False
        else:
            data = json.loads(raw_data)
            new_dict = {}
            for key,val in data.items():
                if (key == 'text'):
                    try:
                        new_dict['text'] = data['extended_tweet']['full_text']
                    except:
                        new_dict['text'] = data['text']
                elif (key == 'created_at') | (key == 'user'):
                    if (key == 'user'):
                        new_dict['name'] = data['user']['name']
                        new_dict['location'] = data['user']['location']
                    else:
                        new_dict[key] = val
            ConnectDb().insert_data(new_dict,self.connection,'RawDb','RawTweets')
            return True
        
    def on_error(self, status_code):
        return False
