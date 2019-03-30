#! /usr/bin/python3
from flask import Flask, make_response, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = [
    {'username': 'Tom', 'password': generate_password_hash('111111')},
    {'username': 'Michael', 'password': generate_password_hash('123456')}
]

@auth.verify_password
def verify_password(username, password):
	for user in users:
		if user['username'] == username:
			if check_password_hash(user['password'], password):
				return True
	return False

@auth.error_handler
def unauth():
	return make_response(jsonify({'error':'Unauthorized acess'}),401)

@app.route('/')
@auth.login_required
def index():
	return 'hello, %s' %auth.username()
app.run()