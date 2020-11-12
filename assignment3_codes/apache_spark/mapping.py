from pymongo import MongoClient
import re
import urllib.parse
from pyspark import SparkContext,SparkConf

'''
Class that applies map reduce logic 
and evaluates the word count
'''
class Mapping():
    def keywords_words(self,keywords):
        #function that converts the keyowords to lowercase
        lower_keywords = []
        for word in keywords:
            lower_keywords.append(word.lower())
        return lower_keywords

    def format_values(self,str_value):
        #function that applies regex and splits the lines
        str_value = re.sub(r'^\W+|\W+$', '', str_value)
        mapped =  map(str.lower, re.split(r'\W+', str_value))
        return mapped


    def access_db(self,client,db,table):
        #function that accesses db and fetches the data for specified collection
        keywords = ['Storm', 'Winter', 'Canada', 'hot', 'cold', 'Flu', 'Snow', 'Indoor', 'Safety', 'rain', 'ice']
        formatted_keywords = self.keywords_words(keywords)
        fopen = open('mapped.txt','w')
        table = client[db][table]
        tweets = table.find()
        for record in tweets:
            for key in record:
                #considering only text key from the database
                if (key == 'TEXT') | (key == 'text'):
                    if(record[key] != None):
                        for word in formatted_keywords:
                            formatted = self.format_values(record[key])
                            if formatted != None:
                                for wrd in formatted:
                                    if wrd == word:
                                        fopen.write(word)
                                        fopen.write('\n')

                    
        fopen.close()

    def word_Count(self,spkContext,client,db,table):
        #map and reduce logic to find the word_count 
        self.access_db(client,db,table)
        found_words = spkContext.textFile('./mapped.txt')
        #setting initial value as 1 for occurrance of the word and reducing the count based on key
        count = found_words.map(lambda word: (word,1)).reduceByKey(lambda value,val:value+val)
        word_count = count.collect()
        fopen = open('wordcount.txt','a')
        fopen.write("Word count for table, {} in the database, {}".format(table,db))
        fopen.write('\n')
        for wc in word_count:
            fopen.write(str(wc))
            fopen.write('\n')
        fopen.close()

                    


if __name__ == "__main__":
    #connecting to the database
    mongo_url = 'mongodb+srv://rashmika5408:'+urllib.parse.quote_plus('Sai@9697')+'@data5408.l9ff0.mongodb.net/bigData?retryWrites=true&w=majority' 
    conn = MongoClient(mongo_url)
    sc = SparkContext('local','WC_Pyspark')
    db_table = {'ProcessDb': 'Tweets', 'ReuterDb': 'Articles'}
    fopen = open('wordcount.txt','w+')
    fopen.truncate(0)
    fopen.close()
    for db,table in db_table.items():

        Mapping().word_Count(sc,conn,db,table)
    conn.close()
