#!/usr/bin/python
# usage : python x.py
# depends on : postgresql server being available

# this program is made to be run incrementally (ie many times without destroying previous run)
# 1. detect and insert objects for images with no objects already detected

# check this code to make a better threaded  : https://github.com/pika/pika/blob/0.12.0/examples/basic_consumer_threaded.py
import sys

import os
import platform
import json
import pika
import logging.config
import time

import threading
import multiprocessing

#local imports
import video_analyzer as video_analyzer

from flask import Flask

app = Flask(__name__,)

@app.route('/')
def index():
    return "Video analyzer console"

@app.route('/health')
def health():
    return ''

analyzer = 'video_speech_to_text'
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

    logger.debug("analyzing video : {} {}".format(image_id, filefullname))
    try:
        try:
            text = video_analyzer.get_text(filefullname)
            logger.debug("text exctracted from speech : {}".format(text))
            if len(text.replace(' ', '')) > 0:
                logger.debug("Pushing OBJ {}".format(obj))
                obj_task = {
                    "filefullname":filefullname,
                    "image_id":image_id,
                    "x":0,
                    "y":0,
                    "w":0,
                    "h":0,
                    "description":"speech_to_text",
                    "confidence":80,
                    "analyzer":analyzer,
                    "analyzer_version":analyzer_version,
                    "derived_from_object":None,
                    "object_image_filename":None,
                    "face_encodings":None,
                    "text_found": text
                }
                post_task(obj_task)
                logger.debug("Pushed OBJ {}".format(obj_task))
        except (Exception) as error:
            obj_task = { "filefullname":filefullname,"description":"error_on_detection","analyzer":analyzer,"analyzer_version":analyzer_version,"image_id":image_id}
            post_task(obj_task)

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
            channel.queue_declare(queue='extractSpeech', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='extractSpeech', on_message_callback=receive, auto_ack=False)

            logger.info(' [*] Waiting for messages on extractText.')
            channel.start_consuming()
        except (Exception) as error:
            logger.error('Rabbitmq connection failed', exc_info=True)
            time.sleep(5)

if __name__ == '__main__':
    logger.info("starting to extract speech")


    def server_start():
        app.run(debug=True, host="0.0.0.0", port=6000)


    p = multiprocessing.Process(target=server_start, args=())
    p.start()


    start()
    logger.info("done")
