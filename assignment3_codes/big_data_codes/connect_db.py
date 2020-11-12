from pymongo import MongoClient
import urllib.parse

'''
class that connects to the mongo database 
and performs insertion, fetching of records 
'''

class ConnectDb(): 
    
    def __init__(self):
        self.url = 'mongodb+srv://rashmika5408:'+ urllib.parse.quote_plus('Sai@9697') + '@data5408.l9ff0.mongodb.net/bigData?retryWrites=true&w=majority'            

    def connect_mongo(self):
        '''
        connect to the mongo database
        '''
        client = MongoClient(self.url)        
        return client
        
    
    def insert_data(self,record,client,db,table):
        '''
        insert record(dict format) into the given table
        '''
        access_db = client[db]
        collection = access_db[table]
        rec = collection.insert_one(record)

    def find_data(self,client,db,table):
        '''
        fetch all the records from the given table
        '''
        access_db = client[db]
        collection = access_db[table]
        data = collection.find()
        return data
