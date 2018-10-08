import os
from flask import Flask

# __file__ refers to the file settings.py 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to app folder
APP_STATIC = os.path.join(APP_ROOT, 'static')

app = Flask(__name__) # run app

@app.route('/')
def read_file():
    with open(os.path.join(APP_STATIC, 'test.txt')) as f: # open file in static 
        file_content = f.read()
    return file_content