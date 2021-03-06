from flask import render_template, flash, redirect, session, url_for, request, g
from main_app import app, conn
import userInfo

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE'
    response.headers['X-XSS-Protection'] = '1'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

@app.route('/')
def main():
    # if the user is logged in, have all the used textfiles available to the user display
    if (session.get('logged_in') == True):
        # query to get all the texts available to the user & feed to dictionary API
        textQuery = 'SELECT Content.id, Content.username, Content.timest, Content.file_path, Content.content_name, Content.file_text\
                    FROM Content\
                    WHERE Content.username= %s\
                    ORDER BY timest desc'

        spellQuery = 'SELECT Wrong.id, Wrong.incorrect_word FROM Wrong'

        try:
            cursor = conn.cursor()
            username = session['username']

            #ids of all the visible posts
            cursor.execute(textQuery, (username))
            textData = cursor.fetchall()
            cursor.execute(spellQuery)
            spellData = cursor.fetchall()
            cursor.close()
        except pymysql.Error as err:
            app.logger.error(err)

        userInfo.initiate()

        return render_template("index.html", data=textData, spellData=spellData)
    return render_template("index.html")

# function to make queries to database to acquire info
def getData(query):
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    return (data)