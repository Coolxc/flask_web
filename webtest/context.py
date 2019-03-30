#!/usr/bin/python3
from flask import Flask, g, request

app = Flask(__name__)

# @app.before_request
# def before_r1():
# 	print('before_request1 start ')
# 	g.name = 'yannn'
# 	return request.url


# @app.after_request
# def after(response):
# 	print('after request finished')
# 	response.headers['Key'] = 'aaa'
# 	return response

# @app.teardown_request
# def teardown(exception):
# 	print('teardown request')
# 	print(request.url)
@app.route('/s/', endpoint='h')
def a():
	return 'helloooo'

@app.route('/ss/')
def a():
	return 'ahahaha'

@app.route('/')
def index():
	return '<h1>endpoint:{}/视图函数：{}</h1>'.format(app.view_functions.keys(),
		app.view_functions.get('hello','None').__name__)
app.run()

