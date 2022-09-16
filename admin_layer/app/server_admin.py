#!/usr/bin/env python
from __future__ import print_function
import sys
from flask import Flask

app = Flask(__name__,)

@app.route('/')
def index():
    return "admin console"

@app.route('/health')
def health():
    return ''

@app.route('/delete_objects/<string:id>')
def delete_objects(id):
    return "deleting objects for : {}".format(id)

@app.route('/detect_objects/<string:id>')
def detect_objects(id):
    return "detecting objects for : {}".format(id)

@app.route('/detect_faces/<string:id>')
def detect_faces(id):
    return "detecting faces for : {}".format(id)

if __name__ == '__main__':
    app.run( debug=True,host="0.0.0.0",port=6000)
    #app.run(debug=True)
