from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import timedelta

app = Flask(__name__) # run app
app.secret_key = 'S3CR3T'

conn = pymysql.connect(host='localhost',
						user='root',
						password='',
						db='spellcheck',
						charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

# give below python files the app
import login, logout, register, main, userInfo, content