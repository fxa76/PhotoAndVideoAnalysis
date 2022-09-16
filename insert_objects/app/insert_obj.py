import psycopg2
import json
import pika
import logging.config
import time

import multiprocessing

#local imports
import connection as dbconnection

from flask import Flask

app = Flask(__name__,)

@app.route('/')
def index():
    return "Objects insert console"

@app.route('/health')
def health():
    return ''

def callback(ch, method, properties, body):
    obj = json.loads(body)
    logger.debug("[x] Received %r" % obj)

    try:
        conn = dbconnection.get_connection()

        myObj = [
            obj['filefullname'],
            obj['image_id'],
            obj['x'],
            obj['y'],
            obj['w'],
            obj['h'],
            obj['description'],
            obj['confidence'],
            obj['analyzer'],
            obj['analyzer_version'],
            obj['derived_from_object'],
            obj['object_image_filename'],
            obj['face_encodings'],
            obj['text_found']
            ]

        insert_obj_query = "INSERT INTO objects (filefullname,image_id,x,y,w,h,description,confidence,analyzer,analyzer_version,derived_from_object,object_image_filename,face_encodings,text_found) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur2 = conn.cursor()
        cur2.execute(insert_obj_query,myObj)
        cur2.close()
        logger.debug("Inserted OBJ {}".format(myObj))
    except(Exception) as error:
        logger.error('Failed to insert', exc_info=True)
    finally:
        if conn is not None:
            conn.close()

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':

    def server_start():
        app.run(debug=True, host="0.0.0.0", port=6000)


    p = multiprocessing.Process(target=server_start, args=())
    p.start()

    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger(__name__)

    credentials = pika.PlainCredentials('mime_engine', '908790172834598012374')
    parameters = pika.ConnectionParameters('rabbitmq',
                                   5672,
                                   '/',
                                   credentials)

    while(True):
        try :
            connection = pika.BlockingConnection(parameters)

            channel = connection.channel()
            channel.queue_declare(queue='addObject', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='addObject', on_message_callback=callback, auto_ack=False)

            logger.info(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        except (Exception) as error:
            logger.error('Rabbitmq connection failed', exc_info=True)
            time.sleep(5)
