from flask import Flask, render_template, request, session, url_for, redirect, abort
import pymysql.cursors
from datetime import timedelta
import logging
from pynput.mouse import Listener

# Setup logging
logging.basicConfig(filename=("logs.txt"), format='[%(levelname)s] %(asctime)s %(name)s %(filename)s:%(lineno)s - %(message)s', level=logging.DEBUG)
flask_logger = logging.getLogger("werkzeug")
flask_logger.setLevel(logging.DEBUG)

app = Flask(__name__) # run app

conn = pymysql.connect(host='localhost',
						user='root',
						password='root',
						db='spellcheck',
						charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

app.logger.info('MYSQL DB successfully connected')

def on_click(x, y, button, pressed):
    if pressed:
        app.logger.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

def on_scroll(x, y, dx, dy):
    app.logger.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))

# give below python files the app
import init, login, logout, register, main, userInfo, content