#! /usr/bin/python3
from flask import Flask

app = Flask(__name__)

@app.route('/aa')
def index():
	return '<h1>do not have the last slash</h1>'

@app.route('/aa/')
def indexs():
	return '<h1>have the last slash</h1>'

app.run()