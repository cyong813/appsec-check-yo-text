from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from main_app import app, conn
import userInfo

@app.route('/register')
def register():
    userInfo.initiate()
    return render_template('register.html')

@app.route('/register/processing', methods=['GET', 'POST'])
def registerProcessing():
    username = request.form['username']
    if username in session['users'].keys():
        errormsg = "Username already taken."
        app.logger.warning('ERR: Duplicate username (%s)', username)
        return render_template('register.html', error = errormsg)
    if len(username) < 6:
        errormsg = "Username is too short. Must be more than 5 characters."
        app.logger.warning('ERR: Short username (%s)', username)
        return render_template('register.html', error = errormsg)
    elif len(username) > 50:
        errormsg = "Username and/or other fields are too long. 50 characters max."
        app.logger.warning('ERR: Long username (%s)', username)
        return render_template('register.html', error = errormsg)

    password = request.form['password']
    if len(password) < 8:
        errormsg = "Password is too short (needs to be greater than 7 characters)."
        app.logger.warning('ERR: Short password (%s)', username)
        return render_template('register.html', error = errormsg)

    upperCase = 0
    lowerCase = 0
    num = 0
    for x in password:
        if x.isupper():
            upperCase = upperCase + 1
        elif x.islower():
            lowerCase = lowerCase + 1
        elif x.isdigit():
            num = num + 1

    if upperCase == 0:
        errormsg = "Password needs to contain at least one uppercase letter."
        app.logger.warning('ERR: Invalid password creation (%s)', password)
        return render_template('register.html', error = errormsg)
    if lowerCase == 0:
        errormsg = "Password needs to contain at least one lowercase letter."
        app.logger.warning('ERR: Invalid password creation (%s)', password)
        return render_template('register.html', error = errormsg)
    if num == 0:
        errormsg = "Password needs to contain at least one number."
        app.logger.warning('ERR: Invalid password creation (%s)', password)
        return render_template('register.html', error = errormsg)
    elif len(password) > 50:
        errormsg = "Password is too long. 50 characters max."
        app.logger.warning('ERR: Invalid password creation (%s)', password)
        return render_template('register.html', error = errormsg)

    retype = request.form['retype']
    if retype != password:
        errormsg = "Passwords do not match."
        app.logger.warning('ERR: Invalid password match (%s, %s)', retype, password)
        return render_template('register.html', error = errormsg)

    firstname = request.form['firstname']
    lastname = request.form['lastname']

    try:
        cursor = conn.cursor()
        query = 'INSERT INTO Person (username, password, first_name, last_name) VALUES (%s, SHA2(%s, 256), %s, %s)'
        cursor.execute(query, (username, password, firstname, lastname))
        conn.commit()
        cursor.close()

        session['logged_in'] = True
        session['username'] = username
        session['users'][username] = {}
        session['users'][username]['first_name'] = firstname
        session['users'][username]['last_name'] = lastname
        
        return redirect(url_for('main', username = session['username']))
    except pymysql.Error as err:
        app.logger.error(err)