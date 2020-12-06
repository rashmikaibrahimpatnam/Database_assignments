import re
import math
import csv
import os
from connect_db import ConnectDB

class SemanticAnalysis():

    def find_word(self,word):    
        articles = ConnectDB().table_data('ReuterDb','Articles')
        wrdcount = 0
        filtered_articles = []
        total_count = articles.count()
        for article in articles: 
            for key in article:
                if key == 'TEXT':                    
                    text = article[key]
                    match = re.search(r'\b{}\b'.format(word),text)
                    if match:
                        wrdcount += 1
                        if word == 'Canada':
                            filtered_articles.append(text)
        if len(filtered_articles) == 0:
            return wrdcount,total_count
        else:
            return wrdcount,total_count,filtered_articles

    def save_to_file(self,data,total_docs=None):
        fields = ['Search Query','Document containing term','Total Documents/number of documents term appeared(df)','Log10(N/df)']
        filename = 'Semantic_Analysis.csv'
        file_exists = os.path.isfile(filename)
        if file_exists:
            with open(filename,'a') as senti:
                writer = csv.writer(senti)
                writer.writerow(data)
            senti.close()
        else:
            with open(filename,'w') as senti:
                writer = csv.writer(senti)
                writer.writerow(['Total number of Documents: {} '.format(total_docs)])
                writer.writerow(fields)
                writer.writerow(data)
            senti.close()
    
    def save_frequency(self,data,total_docs=None):
        fields = ['Term','Canada']
        filename = 'Word_Frequency.csv'
        file_exists = os.path.isfile(filename)
        if file_exists:
            with open(filename,'a') as freq:
                writer = csv.writer(freq)
                writer.writerow(data)
            freq.close()
        else:
            with open(filename,'w') as freq:
                writer = csv.writer(freq)
                writer.writerow(fields)
                writer.writerow(['Canada appeared in {} documents'.format(total_docs),'Total Words(m)','Frequency(f)','Relative frequency(f/m)'])                
                writer.writerow(data)
            freq.close()

    def remove_tags(self,data):
        fetched = re.compile(r'<.*?>')
        return fetched.sub('',data)

    def wrd_frequency(self,filtered_articles):
        frequency_list = []
        if len(filtered_articles) != 0:
            for article in filtered_articles:
                filtered_data = []
                text = self.remove_tags(article)
                tot_wrds = text.split(' ')
                frequency = 0
                for wrd in tot_wrds:
                    wrd = ((wrd.lstrip('<')).rstrip('>')).lower()
                    if wrd == 'canada':
                        frequency += 1
                filtered_data.append(article)
                filtered_data.append(len(tot_wrds))
                filtered_data.append(frequency)
                filtered_data.append(frequency/len(tot_wrds))
                frequency_list.append(frequency/len(tot_wrds))
                self.save_frequency(filtered_data,len(filtered_articles))                    
            rel_freq = max(frequency_list)
            ind = frequency_list.index(rel_freq)
            print(self.remove_tags(filtered_articles[ind]))
    
    def call_word(self):
        lst_words = ['Canada','rain','hot','cold']     
        for wrd in lst_words:
            data = []
            if wrd == 'Canada':
                wordcount,total_count,filtered_articles = self.find_word(wrd)
            else:
                wordcount,total_count = self.find_word(wrd)
            evaluate = total_count/wordcount
            log_val = math.log10(evaluate)
            data.append(wrd)
            data.append(wordcount)
            data.append(round(evaluate,2))
            data.append(round(log_val,2))
            self.save_to_file(data,str(total_count))
        self.wrd_frequency(filtered_articles)


SemanticAnalysis().call_word()
