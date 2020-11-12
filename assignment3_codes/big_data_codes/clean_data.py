import re

'''
class that performs cleaning on the data
'''

class CleanData():

    def clean_spc_articles(self,text):
        #function that removes the special characters from the articles text
        return re.sub(r"[^a-zA-Z0-9<>/]+", ' ',text)

    def clean_spc_chars(self,text):
        #fucntion that removes the special characters from the text
        return re.sub('[^A-Za-z0-9]+', ' ', text)
    
    def clean_url_data(self,text):
        #function that removes the url from the text
        return re.sub(r"http\S+", "", text)
    
    def clean_emoji_data(self,text):
        #function that removes the emoji present in the text
        regex_emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F" 
                           u"\U0001F300-\U0001F5FF"  
                           u"\U0001F680-\U0001F6FF"  
                           u"\U0001F1E0-\U0001F1FF"  
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           u"\U0001f926-\U0001f937"
                           u'\U00010000-\U0010ffff'
                           u"\u200d"
                           u"\u2640-\u2642"
                           u"\u2600-\u2B55"
                           u"\u23cf"
                           u"\u23e9"
                           u"\u231a"
                           u"\u3030"
                           u"\ufe0f"
                           "]+", flags=re.UNICODE)
        return regex_emoji_pattern.sub(r'',text)
