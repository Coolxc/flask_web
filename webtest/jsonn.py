#! /usr/bin/python3
from flask import Flask, jsonify, Response, request
import json

app = Flask(__name__)
@app.route('/json/<name>')
def index(name):
    return jsonify({'Hello':name})

@app.route('/dumps/<name>')
def py(name):
    return json.dumps({'Hello':name})

@app.route('/r')
def r():
	return request.args.get('a')
app.run()