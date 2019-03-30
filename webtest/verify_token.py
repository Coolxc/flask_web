#! /usr/bin/python3
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import Flask, g, jsonify
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
auth = HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(token):
	s = Serializer(app.config['SECRET_KEY'])
	g.user = None
	try:
		data = s.loads(token)
	except:
		return False
	if 'username' in data:
		g.user = data['username']
		return True
	return False

@app.route('/')
@auth.login_required
def index():
	return 'Hello {}'.format(g.user)

@app.route('/get_token/<username>')
def get_token(username):
	s = Serializer(app.config['SECRET_KEY'], expires_in=1800)
	users = ['yang','yu']
	if username in users:
		token = s.dumps({'username':username})
		return '{}的令牌是{}'.format(username,token)
	else:
		return make_response(jsonify({'error':'no user'}),400)

app.run()