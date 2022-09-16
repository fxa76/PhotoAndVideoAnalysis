#!/usr/bin/env python
from __future__ import print_function
import sys
import os

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool

import json
from decimal import Decimal
import decimal
import jsonpickle

from flask import Flask
from flask import render_template
from flask import request

from flask import Flask, flash, request, redirect, url_for

import cv2
import base64
import time
import datetime

#local imports
from fximage import FXImage
from fximageobject import FXImageObject
import fxconnection
import fximageutils

import images_access
import images_search
import find_faces_by_distance

app = Flask(__name__,)

user_name = os.environ['POSTGRES_USER']
password= os.environ['POSTGRES_PASSWORD']
db_name = os.environ['POSTGRES_DB']
host = os.environ['POSTGRES_HOST']
port = os.environ['POSTGRES_PORT']

postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20,user = user_name,
                                              password = password,
                                              host = host,
                                              port = port,
                                              database = db_name)

#fix the issue of non serializable FXImage class.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return o.__dict__

#KEEP returns the file
@app.route('/get_image/<string:id>')
def getimage(id):
    print("get image",file=sys.stderr)
    image = images_access.get_image_by_id(postgreSQL_pool,id)
    image.get_base_64()
    return jsonpickle.encode(image)

@app.route('/get_image_with_overlay/<string:id>')
def getimagewithoverlay(id):
    print("getting overlay image", file = sys.stderr)
    image = images_access.get_image_with_objects_by(postgreSQL_pool,id)
    image.get_base_64_overlayed()
    #print(image,file = sys.stderr)
    return jsonpickle.encode(image)

@app.route('/update_image',methods=['PUT'])
def updateImage():
    json_received = request.get_json()
    print("trying to update IMAGE data comments is : {}".format(json_received['comments']), file=sys.stderr)
    print("trying to update IMAGE data timestamp is : {}".format(json_received['timestamp']), file=sys.stderr)
    try:
        sql = "UPDATE Images set comments=%s, lat=%s,lon=%s, timestamp=%s, creationdate=%s where image_id=%s"
        print("sql : {}".format(sql),file=sys.stderr)
        conn = postgreSQL_pool.getconn()
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql,(json_received['comments'],json_received['lat'],json_received['lon'],json_received['timestamp'],json_received['creationdate'],json_received['image_id'],))
    except(Exception) as error:
        print("error while updating image",file=sys.stderr)
    finally:
        cur.close()
        postgreSQL_pool.putconn(conn)

    return  json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/get_similiar_aces_to/<string:id>')
def get_similar_faces(id):
    return jsonpickle.encode(find_faces_by_distance.get_similar_to_id(id))

@app.route('/health')
def health():
    return ''

@app.route('/')
def index():

    return render_template('index.html', title='Home')

if __name__ == '__main__':
    app.run( debug=True,host="0.0.0.0",port=5000)
