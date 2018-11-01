import os
from flask import Flask, render_template, request
import pymysql.cursors

app = Flask(__name__) # run app

conn = pymysql.connect(host='localhost',
						user='root',
						password='',
						db='spellcheck',
						charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

# @app.route('/')
# def read_file():
#     with open(os.path.join(APP_STATIC, 'test.txt')) as f: # open file in static, assuming it's a .txt off the bat
#         file_content = f.read()
#     return file_content

# @app.route('/check')
# def check_spelling():
#     wrong_words = set()
#     with open(os.path.join(APP_STATIC, 'test.txt')) as f: # open file in static, assuming it's a .txt off the bat
#         word_list = [word for line in f for word in line.split()] # extract all words into arr
    
#     for word in word_list:
#         if (isWordInDictionary(word.lower()) != 200):
#             wrong_words.add(word)
#     return "Found "+str(len(wrong_words))+" error: "+str(wrong_words)