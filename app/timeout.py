import datetime, flask, flask_login

#logouts after a period of inactivity 

@app.before_request
def before_request():
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=15) #timer for 15mins
    flask.session.modified = True  #resets the seeions
    flask.g.user = flask_login.current_user