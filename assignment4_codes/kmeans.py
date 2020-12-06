from connect_db import ConnectDB
import datetime
import os
import csv

class DataAnalysis():
    def save_to_file(self,data):
        fields = ['TimestampId','Timestamp']
        filename = 'Timestamp.csv'
        file_exists = os.path.isfile(filename)
        if file_exists:
            with open(filename,'a') as timestp:
                writer = csv.writer(timestp)
                writer.writerow(data)
            timestp.close()
        else:
            with open(filename,'w') as timestp:
                writer = csv.writer(timestp)
                writer.writerow(fields)
                writer.writerow(data)
            timestp.close()

    def fetch_data(self):
        tweets = ConnectDB().table_data('ProcessDb','Tweets')
        tweet_txt = []
        count = 0
        for tweet in tweets:
            for key in tweet:
                if key == 'created_at':
                    timestp = []
                    converted = datetime.datetime.strptime(tweet[key], '%a %b %d %H %M %S 0000 %Y').strftime('%Y-%m-%d %H:%M:%S')
                    count += 1
                    timestp.append(count)
                    timestp.append(datetime.datetime.strptime(converted,'%Y-%m-%d %H:%M:%S').timestamp())
                    self.save_to_file(timestp)

DataAnalysis().fetch_data()



