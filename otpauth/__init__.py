__version__ = '0.1.0'

from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello!</h1>'


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))
