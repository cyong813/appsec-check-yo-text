import datetime, flask, flask_login
from main_app import app, conn

#logouts after a period of inactivity 

@app.before_request
def before_request():
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=15) # timer for 15mins
    flask.session.modified = True  # resets the sessions
    flask.g.user = flask_login.current_user