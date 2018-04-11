#!/usr/bin/env python3

from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        data = {'lol': 22, 'kek': 42, 'cheburek': 239}
        return jsonify(data)
    return 'Error'
git