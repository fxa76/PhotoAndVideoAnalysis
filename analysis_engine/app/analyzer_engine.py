#!/usr/bin/python
# usage : python x.py
# depends on : postgresql server being available

# this program is made to be run incrementally (ie many times without destroying previous run)
# 1. detect and insert objects for images with no objects already detected

# check this code to make a better threaded  : https://github.com/pika/pika/blob/0.12.0/examples/basic_consumer_threaded.py

import os
import json
import pika
import logging.config
import time

import threading
import multiprocessing

from analysis_engine.app import fx_analyzer

# local imports
from analyser import fx_analyzer

from flask import Flask


app = Flask(__name__,)

@app.route('/')
def index():
    return "analysis engine console"

@app.route('/health')
def health():
    return ''

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

pika_username = os.environ['RABBITMQ_USERNAME']
pika_password = os.environ['RABBITMQ_PWD']
pika_server = os.environ['RABBITMQ_SERVER']

pika_listen_queue =  os.environ['RABBITMQ_LISTEN_QUEUE'] #'test_wait_queue'
pika_add_object_queue = os.environ['RABBITMQ_POST_QUEUE'] #'test_post_queue'

pika_rabbit_server_port = 5672


def post_task(obj_arr) -> None :
    try:
        credentials = pika.PlainCredentials(pika_username, pika_password)
        parameters = pika.ConnectionParameters(pika_server, pika_rabbit_server_port, '/', credentials)
        connection_out = pika.BlockingConnection(parameters)
        channel_out = connection_out.channel()
        channel_out.queue_declare(queue=pika_add_object_queue, durable=True)

        for obj in obj_arr:
            channel_out.basic_publish(exchange='',
                                      routing_key=pika_add_object_queue,
                                      body=json.dumps(obj.__dict__),
                                      properties=pika.BasicProperties(
                                          content_type='application/json',
                                          content_encoding='utf-8',
                                          delivery_mode=2  # make message persistent
                                      ))
        connection_out.close()
    except (Exception) as error:
        logger.debug("error while posting objs image", exc_info=True)

def get_file(image_id):
    import requests

    url = 'https://fxalap/fs/v1/get_file/{}'.format(image_id)
    r = requests.get(url, allow_redirects=True, verify=False)

    r.content


def analysis_call_back(body) -> None:
    try:
        obj = json.loads(body)

        image_id = obj['image_id']

        logger.debug("analyzing image id {} ".format(image_id))

        obj_task_array = fx_analyzer.perform_task(image_id)
        logger.debug("objects returned {}".format(obj_task_array))
        post_task(obj_task_array)

    except (Exception) as error:
        logger.debug("error while processing image", exc_info=True)


def receive(ch, method, properties, body) -> None:
    logger.debug("rabbitmq receiver")
    t = threading.Thread(target=analysis_call_back, args=(body,))
    t.daemon = True
    t.start()

    while t.is_alive():
        logger.debug("[INFO] heart beating")
        ch.connection.process_data_events()
        ch.connection.sleep(5)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    logger.debug("done")


def start() -> None:
    credentials = pika.PlainCredentials(pika_username, pika_password)
    parameters = pika.ConnectionParameters(pika_server, pika_rabbit_server_port, '/', credentials)

    while (True):
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            # declare queue if it is not yet declared
            channel.queue_declare(queue=pika_listen_queue, durable=True)

            # setup fetch 1 by 1
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=pika_listen_queue, on_message_callback=receive, auto_ack=False)

            logger.info(' [*] Waiting for messages on {}. To exit press CTRL+C'.format(pika_listen_queue))
            channel.start_consuming()
        except (Exception) as error:
            logger.error('Rabbitmq connection failed', exc_info=True)
            time.sleep(5)


if __name__ == '__main__':
    logger.info("starting health check server")

    # start server for API healthchecks.
    def server_start():
        app.run(debug=True, host="0.0.0.0", port=6000)


    p = multiprocessing.Process(target=server_start, args=())
    p.start()

    logger.info("starting rabbitmq reader loop")
    start()

    logger.info("Exiting")
