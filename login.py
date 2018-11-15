from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from main_app import app, conn

@app.route('/login')
def login():
    return render_template('login.html')

# authenticates logins
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    username = request.form['username']
    password = request.form['password']

    cursor = conn.cursor()
    query = 'SELECT * FROM Person WHERE username = %s and password = SHA2(%s, 256)'
    cursor.execute(query, (username, password))
    #stores results in var
    data = cursor.fetchone()
    cursor.close()

    if (data):
        session['logged_in'] = True
        session['username'] = username
        session.permanent = False
        return redirect(url_for('main', username=session['username']))
    else:
        error = "Invalid login or username/password"
    return render_template('login.html', error=error)