#!/usr/bin/python
# usage : python x.py
# depends on : postgresql server being available

# this program is made to be run incrementally (ie many times without destroying previous run)
# 1. detect and insert objects for images with no objects already detected

# check this code to make a better threaded  : https://github.com/pika/pika/blob/0.12.0/examples/basic_consumer_threaded.py

import json
import logging.config
import time
import os
import cv2
import pika
import pytesseract
from flask import Flask
from pytesseract import Output

import multiprocessing
import threading

app = Flask(__name__,)

@app.route('/')
def index():
    return "Text extraction console"

@app.route('/health')
def health():
    return ''

analyzer = 'object_ocr'
analyzer_version = 100

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
    connection_out = pika.BlockingConnection(parameters)
    channel_out = connection_out.channel()
    channel_out.queue_declare(queue='addObject', durable=True)
    channel_out.basic_publish(exchange='',
                          routing_key='addObject',
                          body=json.dumps(obj),
                          properties=pika.BasicProperties(
                            content_type='application/json',
                            content_encoding='utf-8',
                            delivery_mode = 2 # make message persistent
                        ))
    connection_out.close()

def detect_text(ch, method, properties, body):
    obj = json.loads(body)
    filefullname = obj['filefullname']
    image_id = obj['image_id']

    logger.debug("analyzing image : {} {}".format(image_id, filefullname))
    try:
        try:
            im = cv2.imread(filefullname, cv2.IMREAD_COLOR)
            rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            # Run tesseract OCR on image
            h, w, c = rgb.shape
            d = pytesseract.image_to_data(rgb, output_type=Output.DICT)
            n_boxes = len(d['text'])
            if n_boxes == 0 :
                obj_task = {
                    "filefullname": filefullname,
                    "image_id": image_id,
                    "x": 0,
                    "y": 0,
                    "w": 0,
                    "h": 0,
                    "description": "no_text_found",
                    "confidence": 1,
                    "analyzer": analyzer,
                    "analyzer_version": analyzer_version,
                    "derived_from_object": None,
                    "object_image_filename": None,
                    "face_encodings": None,
                    "text_found": None
                }
                post_task(obj_task)
                logger.debug("Pushed OBJ {}".format(obj_task))
            else:
                for i in range(n_boxes):
                    #needed to avoid insertion of space only
                    if len(d['text'][i].replace(' ', '')) > 0:
                        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                        logger.debug("Pushing OBJ {}".format(obj))
                        obj_task = {
                            "filefullname":filefullname,
                            "image_id":image_id,
                            "x":x,
                            "y":y,
                            "w":w,
                            "h":h,
                            "description":"text_found",
                            "confidence":d['conf'][i],
                            "analyzer":analyzer,
                            "analyzer_version":analyzer_version,
                            "derived_from_object":None,
                            "object_image_filename":None,
                            "face_encodings":None,
                            "text_found": d['text'][i]
                        }
                        post_task(obj_task)
                        logger.debug("Pushed OBJ {}".format(obj_task))
        except (Exception) as error:
            obj_task = {
                "filefullname": filefullname,
                "image_id": image_id,
                "x": 0,
                "y": 0,
                "w": 0,
                "h": 0,
                "description": "error_on_text_detection",
                "confidence": d['conf'][i],
                "analyzer": analyzer,
                "analyzer_version": analyzer_version,
                "derived_from_object": None,
                "object_image_filename": None,
                "face_encodings": None,
                "text_found": None
            }
            post_task(obj_task)
            logger.debug("Pushed OBJ {}".format(obj_task))

    except (Exception) as error:
        logger.debug("error while processing image", exc_info=True)



def receive(ch, method, properties, body):
        logger.debug("""rabbitmq receiver""")
        t = threading.Thread(target=detect_text, args=(ch, method, properties, body,))
        t.daemon = True
        t.start()

        while t.is_alive():
            logger.debug("[INFO] heart beating")
            ch.connection.process_data_events()
            ch.connection.sleep(5)

        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.debug("done")

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
            channel.queue_declare(queue='extractText', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='extractText', on_message_callback=receive, auto_ack=False)

            logger.info(' [*] Waiting for messages on extractText.')
            channel.start_consuming()
        except (Exception) as error:
            logger.error('Rabbitmq connection failed', exc_info=True)
            time.sleep(5) 

if __name__ == '__main__':
    logger.info("starting to extract text")


    def server_start():
        app.run(debug=True, host="0.0.0.0", port=6000)


    p = multiprocessing.Process(target=server_start, args=())
    p.start()

    start()
    logger.info("done")
