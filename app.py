import os
from flask import Flask
import requests

# __file__ refers to the file settings.py 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to app folder
APP_STATIC = os.path.join(APP_ROOT, 'static')

app = Flask(__name__) # run app

# Application keys for Oxford dictionary API
app_id = ''
app_key = ''
language = ''

def isWordInDictionary(lower_word):
        url = ('https://od-api.oxforddictionaries.com/api/v1/inflections/'
               + language + '/' + lower_word)
        r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
        return r.status_code

@app.route('/')
def read_file():
    with open(os.path.join(APP_STATIC, 'test.txt')) as f: # open file in static, assuming it's a .txt off the bat
        file_content = f.read()
    return file_content

@app.route('/check')
def check_spelling():
    wrong_words = set()
    with open(os.path.join(APP_STATIC, 'test.txt')) as f: # open file in static, assuming it's a .txt off the bat
        word_list = [word for line in f for word in line.split()] # extract all words into arr
    
    for word in word_list:
        if (isWordInDictionary(word.lower()) != 200):
            wrong_words.add(word)
    return "Found "+str(len(wrong_words))+" error: "+str(wrong_words)