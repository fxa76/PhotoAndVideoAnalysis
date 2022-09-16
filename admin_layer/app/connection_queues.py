# common setup for RabbitMq connections
import json
import pika
import os


def post_task(obj,queue):
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
    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=json.dumps(obj),
                          properties=pika.BasicProperties(
                            content_type='application/json',
                            content_encoding='utf-8',
                            delivery_mode = 2 # make message persistent
                        ))
    connection.close()