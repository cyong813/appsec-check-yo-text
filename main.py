from flask import render_template, flash, redirect, session, url_for, request, g
from main_app import app, conn
import userInfo

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/')
def main():
    #return render_template('result.html', data=session['users'])
    # if the user is logged in, have all the used textfiles available to the user display
    if (session.get('logged_in') == True):
        # query to get all the posts available to the user

        cursor = conn.cursor()
        username = session['username']

        userInfo.initiate()
        
        return render_template("index.html")
    return render_template("index.html")

# function to make queries to database to acquire info
def getData(query):
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    return (data)