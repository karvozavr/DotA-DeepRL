#!/usr/bin/env python3

from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        data = {'test1': 22, 'test2': 42, 'test3': 239}
        return jsonify(data)
    return 'Error'
