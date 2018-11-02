from flask import Flask, render_template, request, session, url_for, redirect
from main_app import app
import main, login, logout
import pymysql.cursors
from datetime import timedelta

app.secret_key = 'S3CR3T'

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

if __name__ == "__main__":
    app.run('localhost', 5000, debug = True)