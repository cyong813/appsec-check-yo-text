from flask import render_template, flash, redirect, session, url_for, request, g
from main_app import app, conn

def initiate():
    # get all the users
    userQuery = 'SELECT username, first_name, last_name FROM person'
    userData = getData(userQuery)
    storeUsers(userData)

def getData(query):
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.commit()
    cursor.close()
    return (data)

def storeUsers(data):
    # store users in a session users dictionary
    # which can be used to access users' first name and last name.
    session['users'] = {}
    for user in data:
        session['users'][user['username']] = {}
        session['users'][user['username']]['first_name'] = user['first_name']
        session['users'][user['username']]['last_name'] = user['last_name']
    return