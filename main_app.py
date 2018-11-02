from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import timedelta

app = Flask(__name__) # run app
app.secret_key = 'S3CR3T'

conn = pymysql.connect(host='localhost',
						user='root',
						password='',
						db='spellcheck',
						charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

# give below python files the app
import login, logout, register, main, userInfo, content

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