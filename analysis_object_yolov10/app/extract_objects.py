#!/usr/bin/python
# usage : python x.py
# depends on : postgresql server being available

# this program is made to be run incrementally (ie many times without destroying previous run)
# 1. detect and insert objects for images with no objects already detected

import sys

import os
import platform
import cv2
import json
import pika
import logging.config
import time
from ultralytics import YOLO

model = YOLO("yolov10x.pt")

import multiprocessing

from flask import Flask

app = Flask(__name__,)

@app.route('/')
def index():
    return "objects extraction console"

@app.route('/health')
def health():
    return ''

analyzer = 'object_detector_yolov10'
analyzer_version = 210

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

def post_task(obj):
    username = os.environ['RABBITMQ_USERNAME']
    pwd = os.environ['RABBITMQ_PWD']
    server = os.environ['RABBITMQ_SERVER']

    credentials = pika.PlainCredentials(username, pwd)
    parameters = pika.ConnectionParameters(server,
                                   5672,
                                   '/',
                                   credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='addObject', durable=True)
    channel.basic_publish(exchange='',
                          routing_key='addObject',
                          body=json.dumps(obj),
                          properties=pika.BasicProperties(
                            content_type='application/json',
                            content_encoding='utf-8',
                            delivery_mode = 2 # make message persistent
                        ))
    connection.close()

def detect_objects(ch, method, properties, body):
    obj = json.loads(body)
    filefullname = obj['filefullname']
    image_id = obj['image_id']

    logger.debug("analyzing image : {} {}".format(image_id, filefullname))
    try:
        # read input image
        image = cv2.imread(filefullname)
        objects_list=[]
        # apply object detection
        try:
            results = model(image)
            cls = results[0].boxes.cls
            xywh = results[0].boxes.xywh.numpy()
            conf = results[0].boxes.conf

            if len(cls)==0:
                objects_list.append( [ filefullname,0,0,0,0,"nothing_found",1,analyzer,analyzer_version,image_id])

            i=0
            for c in cls:
                print(c)
                label = model.names[c.item()]
                x=int(xywh[i][0]-xywh[i][2]/2)
                y=int(xywh[i][1]-xywh[i][3]/2)
                w=int(xywh[i][2])
                h=int(xywh[i][3])
                confidence=conf[i].item()
                logger.debug(f"label: {label}, xywh{x}{y}{w}{h}, conf {confidence}") 
                objects_list.append( [ filefullname,x,y,w,h,label,confidence, analyzer, analyzer_version,image_id])
                i+=1
            
            

        except (Exception) as error:
            logger.error(error)
            objects_list.append( [ filefullname,0,0,0,0,"error_on_detection",1,analyzer,analyzer_version,image_id])

        for obj in objects_list:
            logger.debug("Pushing OBJ {}".format(obj))
            obj_task = {
                "filefullname":obj[0],
                "image_id":obj[9],
                "x":obj[1],
                "y":obj[2],
                "w":obj[3],
                "h":obj[4],
                "description":obj[5],
                "confidence":obj[6],
                "analyzer":analyzer,
                "analyzer_version":analyzer_version,
                "derived_from_object":None,
                "object_image_filename":None,
                "face_encodings":None,
                "text_found": None
            }
            post_task(obj_task)
            logger.debug("Pushed OBJ {}".format(obj_task))

    except (Exception) as error:
        logger.debug("error while processing image", exc_info=True)

    ch.basic_ack(delivery_tag=method.delivery_tag)

def start():
    username = os.environ['RABBITMQ_USERNAME']
    pwd = os.environ['RABBITMQ_PWD']
    server = os.environ['RABBITMQ_SERVER']

    credentials = pika.PlainCredentials(username, pwd)
    parameters = pika.ConnectionParameters(server,
                                   5672,
                                   '/',
                                   credentials)

    while(True):
        try :
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue='extractObjectsYolov10', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='extractObjectsYolov10', on_message_callback=detect_objects, auto_ack=False)

            logger.info(' [*] Waiting for messages on extractObjects.')
            channel.start_consuming()
        except (Exception) as error:
            logger.error('Rabbitmq connection failed', exc_info=True)
            time.sleep(5) 

if __name__ == '__main__':
    logger.info("starting to extract objects")


    def server_start():
        app.run(debug=True, host="0.0.0.0", port=6000)


    p = multiprocessing.Process(target=server_start, args=())
    p.start()

    start()
    logger.info("done")
