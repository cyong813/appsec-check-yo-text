from flask import send_from_directory, render_template, flash, redirect, session, url_for, request, g
from appdef import app, conn
import main, time, datetime, os
from appdef import app
from werkzeug.utils import secure_filename

# Application keys for Oxford dictionary API
app_id = ''
app_key = ''
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
    query = "SELECT * FROM content WHERE username=%s"
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

    if not allowed_file(request.files['text'].filename):
        error = 'Please attach text files only.'
        return render_template('checkText.html', error=error)

    if request.method == 'POST' and 'text' in request.files:
        submitted_file = request.files['text']
        filename = submitted_file.save(request.files['text'])
        txt_filepath = txt_filepath + filename

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

    query = 'INSERT into Content (id, username, timest, txt_filepath, content_name, public) values (%s, %s, %s, %s, %s, %s)'
    cursor.execute(query, (textID, username, timest, txt_filepath, content_name, public))
    conn.commit()
    cursor.close()
    return redirect(url_for('main'))

def getData(query):
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data
