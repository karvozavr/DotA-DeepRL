#!/usr/bin/env python3
import time
import random

from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        data = [random.randrange(-10.0, 10.0),  random.randrange(-10.0, 10.0)]
        print(request.get_data(as_text=True))
        return jsonify(data)
    return 'Error'
