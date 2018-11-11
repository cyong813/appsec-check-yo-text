from flask import send_from_directory, render_template, flash, redirect, session, url_for, request, g
from main_app import app, conn
import main, time, datetime, os, requests
from werkzeug.utils import secure_filename

# Application keys for Oxford dictionary API
app_id = ''
app_key = ''
language = ''

def isWordInDictionary(lower_word):
    url = ('https://od-api.oxforddictionaries.com/api/v1/inflections/'
           + language + '/' + lower_word)
    r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
    return r.status_code

def searchWordInDictionary(lower_word):
    url = ('https://od-api.oxforddictionaries.com/api/v1/search/'
           + language + '/' + lower_word)
    r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
    return r

ALLOWED_EXTENSIONS = set(['txt'])
app.config['UPLOAD_FOLDER'] = 'static'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# displays all texts that went thru spellchecker
@app.route('/texts')
def texts():
    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    query = "SELECT * FROM Content WHERE username=%s"
    cursor = conn.cursor()
    cursor.execute(query, (session['username']))
    data = cursor.fetchall()
    cursor.close()
    return render_template('texts.html', data=data)

# user pastes text here 
@app.route('/checkText/')
def checkText():
    if (not session.get('logged_in')):
        return redirect(url_for('main'))
    return render_template('checkText.html')

# pasted text is processed to return result page with errors and suggestions
@app.route('/checkText/processing', methods=['GET', 'POST'])
def checkTextProcessed():
    if (not session.get('logged_in')):
        return redirect(url_for('main'))

    content_name = request.form['content_name']

    if len(content_name) > 50:
        error = 'Title is too long. 50 characters max.'
        return render_template('checkText.html', error=error)

    txt_filepath = '/static/'

    try:
        file = request.files['text']
    except:
        file = None

    if not allowed_file(file.filename):
        error = 'Please attach text files only.'
        return render_template('checkText.html', error=error)

    wrong_words = set()

    if request.method == 'POST' and file != None:
        # save the text file in static folder
        submitted_file = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], submitted_file))
        txt_filepath = txt_filepath + submitted_file

        # read the file and retrieve text
        with open(os.path.join(app.config['UPLOAD_FOLDER'], submitted_file), 'r') as input_file:
            file_text = input_file.read()
        
        word_list = file_text.split() # extract all words into arr
        # print(word_list)
        
        for word in word_list:
            if (isWordInDictionary(word.lower()) != 200):
                wrong_words.add(word)

    username = session['username']
    cursor = conn.cursor()
    timest = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    query = 'SELECT max(id) as textID FROM Content' #to get the id of this post
    cursor.execute(query)
    textID = cursor.fetchone()['textID'] # + 1
    
    if (textID is None):
        textID = 1
    else:
        textID += 1

    query = 'INSERT into Content (id, username, timest, file_path, content_name, file_text) values (%s, %s, %s, %s, %s, %s)'
    cursor.execute(query, (textID, username, timest, txt_filepath, content_name, file_text))

    # retrieve set of incorrectly spelled words and push into Wrong 
    for word in wrong_words:
        query = 'INSERT into Wrong (id, incorrect_word) values (%s, %s)'
        cursor.execute(query, (textID, word))

    conn.commit()
    cursor.close()
    return redirect(url_for('main'))

def getData(query):
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data
