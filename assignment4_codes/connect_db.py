from pymongo import MongoClient
import urllib.parse

class ConnectDB():   
    def __init__(self):
        self.url = 'mongodb+srv://rashmika5408:'+ urllib.parse.quote_plus('Sai@9697') + '@data5408.l9ff0.mongodb.net/bigData?retryWrites=true&w=majority'            

    def connect_mongo(self):
        client = MongoClient(self.url)        
        return client
    
    def table_data(self,DB,collection):
        client = self.connect_mongo()
        table = client[DB][collection]
        data_in_tables = table.find()
        client.close()
        return data_in_tables
    