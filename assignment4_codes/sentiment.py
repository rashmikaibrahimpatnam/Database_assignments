from pymongo import MongoClient
import urllib.parse
import csv
import os
from connect_db import ConnectDB

class SentiAnalysis(): 
    
    def find_polarity(self):
        fopen = open("wordpolarity.csv",'r')
        lines = fopen.readlines()
        polarity_dict = {}
        for line in lines:
            polarity = line.split(',')
            if 'Polarity' not in line:
                polar = polarity[1].strip('\n')
                word = polarity[0].lower()
                polarity_dict[word] = polar
        return polarity_dict
    
    def save_to_file(self,data):
        fields = ['Message/Tweets','Match','Polarity']
        filename = 'Sentiment_Analysis.csv'
        file_exists = os.path.isfile(filename)
        if file_exists:
            with open(filename,'a') as senti:
                writer = csv.writer(senti)
                writer.writerow(data)
            senti.close()
        else:
            with open(filename,'w') as senti:
                writer = csv.writer(senti)
                writer.writerow(fields)
                writer.writerow(data)
            senti.close()

    
    def eval_score(self,word_dict,tweet):
        polarity = self.find_polarity()            
        score = 0
        match = []
        data = []
        for wrd in word_dict:
            if wrd in polarity:
                match.append(wrd)
                score = score + int(polarity[wrd])
        if len(match) != 0:
            if score > 1:            
                data.append(tweet)
                data.append(match)
                data.append('positive') 
            elif score < -1:
                data.append(tweet)
                data.append(match)
                data.append('negative') 
            else:
                data.append(tweet)
                data.append(match)
                data.append('neutral') 
            self.save_to_file(data)                    
    
    def find_tweets(self):        
        tweets = ConnectDB().table_data('ProcessDb','Tweets')
        tweet_txt = []
        for tweet in tweets:
            for key in tweet:
                if key == 'text':
                    word_dict = {}
                    txt = tweet[key]
                    if txt in tweet_txt:
                        pass
                    else:
                        tweet_txt.append(txt)
                        words = txt.split(' ')
                        for word in words:
                            word = word.lower()
                            if word == '':
                                pass
                            elif word in word_dict:
                                #word present
                                count = word_dict[word] 
                                count = count+1
                                word_dict[word] = count
                            else:
                                #word not present
                                word_dict[word] = 1
                        self.eval_score(word_dict,tweet['text'])

SentiAnalysis().find_tweets()
