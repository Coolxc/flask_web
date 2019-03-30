#!/usr/bin/python3
from flask import Flask, current_app

app = Flask(__name__)

with app.app_context():
	print(current_app.name)
@app.route('/')
def index():
	return 'hello %s' %current_app.name

app.run()