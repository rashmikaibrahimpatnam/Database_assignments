import re
from connect_db import ConnectDb
from clean_data import CleanData

'''
Class that fetches the content between
the news article tags present in the 
sgm files
'''

class Articles():
    def __init__(self,connect):
        self.connect = connect

    def parse_file(self,sgmfiles):
        '''
        accesses the given files and finds the 
        content between the required tags
        '''

        for filename in sgmfiles:
            fopen = open(filename,'r')
            lines = fopen.read()
            fopen.close()
            pattern = "<REUTERS[^>]*>([\s\S]*?)</REUTERS>"
            reuters = re.findall(pattern,lines)
            for line in reuters:            
                rec_dict = {}
                #removing special characters from the obtained text
                line = CleanData().clean_spc_articles(line)
                rec_dict['REUTERS'] = line
                t_pttrn = "<TITLE>(.*?)</TITLE>"
                title = re.findall(t_pttrn,line)
                if len(title) != 0:
                    title = CleanData().clean_spc_articles(title[0])
                rec_dict['TITLE'] = title
                txt_pttrn = "<TEXT[^>]*>([\s\S]*?)</TEXT>"
                text = re.findall(txt_pttrn,line)
                if len(text) != 0:
                    text = CleanData().clean_spc_articles(text[0])
                rec_dict['TEXT'] = text
                #inserting each article into the database into the Articles collection
                ConnectDb().insert_data(rec_dict,self.connect,'ReuterDb','Articles')
      
if __name__ == "__main__":
    conn = ConnectDb().connect_mongo()
    articles = Articles(conn)
    files_with_articles = ['reut2-009.sgm','reut2-014.sgm']
    articles.parse_file(files_with_articles)
    conn.close()

