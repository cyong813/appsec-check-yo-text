from flask import Flask, render_template, request, session, url_for, redirect, abort
from main_app import app
import main, login, logout
import pymysql.cursors
from datetime import timedelta

# created using 
# import os
# os.urandom(24)
app.secret_key = b'@v\x7f\xbd\xa5]5\xec\x19g\x99C\xc4/N\x7f\x14\x07)\x85\x11O\xcd\r'

def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = 'S3CR3T'
    return session['_csrf_token']

app.add_template_global(name='csrf_token', f=generate_csrf_token)

if __name__ == "__main__":
    # add ssl to encrypt to https (req pyopenssl)
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True, ssl_context='adhoc')
    with Listener(on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()