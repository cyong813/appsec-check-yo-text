from flask import send_from_directory, render_template, flash, redirect, session, url_for, request, g
from main_app import app, conn
import main, time, datetime, os, requests
from werkzeug.utils import secure_filename

# Application keys for Oxford dictionary API
app_id = '39c9cb2a'
app_key = '4047c80e6900d9c66c4ec63ba258acdc'
language = 'en'

def isWordInDictionary(lower_word):
    url = ('https://od-api.oxforddictionaries.com/api/v1/inflections/'
           + language + '/' + lower_word)
    r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
    return r.status_code

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

    if request.method == 'POST' and file != None:
        # save the text file in static folder
        submitted_file = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], submitted_file))
        txt_filepath = txt_filepath + submitted_file

        # read the file and retrieve text
        with open(os.path.join(app.config['UPLOAD_FOLDER'], submitted_file), 'r') as input_file:
            file_text = input_file.read()
        
        wrong_words = set()
        word_list = file_text.split() # extract all words into arr
        print(word_list)
        
        for word in word_list:
            if (isWordInDictionary(word.lower()) != 200):
                wrong_words.add(word)

        # retrieve set of incorrectly spelled words
        wrong_word_list = str(wrong_words)

        # fix file_text to make html (bold red for incorrect words)
        result_text = ""
        for word in word_list:
            if word in wrong_word_list:
                result_text += " [ " + word + " ] "
            else:
                result_text += " " + word + " "
        # print(result_text)

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

    query = 'INSERT into Content (id, username, timest, file_path, content_name, file_text, wrong_word_list) values (%s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(query, (textID, username, timest, txt_filepath, content_name, result_text, wrong_word_list))
    conn.commit()
    cursor.close()
    return redirect(url_for('main'))

def getData(query):
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data
