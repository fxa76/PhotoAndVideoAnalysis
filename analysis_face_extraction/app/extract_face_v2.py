#!/usr/bin/python
# The contents of this file are in the public domain. See LICENSE_FOR_EXAMPLE_PROGRAMS.txt
#
#   This example shows how to use dlib's face recognition tool.  This tool maps
#   an image of a human face to a 128 dimensional vector space where images of
#   the same person are near to each other and images from different people are
#   far apart.  Therefore, you can perform face recognition by mapping faces to
#   the 128D space and then checking if their Euclidean distance is small
#   enough.
#
#   When using a distance threshold of 0.6, the dlib model obtains an accuracy
#   of 99.38% on the standard LFW face recognition benchmark, which is
#   comparable to other state-of-the-art methods for face recognition as of
#   February 2017. This accuracy means that, when presented with a pair of face
#   images, the tool will correctly identify if the pair belongs to the same
#   person or is from different people 99.38% of the time.
#
#   Finally, for an in-depth discussion of how dlib's tool works you should
#   refer to the C++ example program dnn_face_recognition_ex.cpp and the
#   attendant documentation referenced therein.
#
#
#
#
# COMPILING/INSTALLING THE DLIB PYTHON INTERFACE
#   You can install dlib using the command:
#       pip install dlib
#
#   Alternatively, if you want to compile dlib yourself then go into the dlib
#   root folder and run:
#       python setup.py install
#
#   Compiling dlib should work on any operating system so long as you have
#   CMake installed.  On Ubuntu, this can be done easily by running the
#   command:
#       sudo apt-get install cmake
#
#   Also note that this example requires Numpy which can be installed
#   via the command:
#       pip install numpy

# file downloaded from http://dlib.net/face_recognition.py.html
import sys
import os
import dlib
import glob
import cv2
import numpy as np
import json
import pika
import logging.config
import time

import threading
import multiprocessing

from flask import Flask

app = Flask(__name__,)

@app.route('/')
def index():
    return "face extraction console"

@app.route('/health')
def health():
    return ''


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)
analyzer = 'face_detector_v2'
analyzer_version = 200
predictor_path = "./data_networks/shape_predictor_5_face_landmarks.dat"
face_rec_model_path = "./data_networks/dlib_face_recognition_resnet_model_v1.dat"
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)

#convert  dlib vector to array compatible with postgres list
def dlib_vect_to_array(vector):
    array = [0]*128
    for i in range(0, len(vector)):
        array[i] = vector[i]
    return array

def post_task(obj):
    username = os.environ['RABBITMQ_USERNAME']
    pwd = os.environ['RABBITMQ_PWD']
    server = os.environ['RABBITMQ_SERVER']

    credentials = pika.PlainCredentials(username, pwd)
    parameters = pika.ConnectionParameters(server,
                                   5672,
                                   '/',
                                   credentials)
    connection2 = pika.BlockingConnection(parameters)
    channel2 = connection2.channel()
    channel2.queue_declare(queue='addObject', durable=True)
    channel2.basic_publish(exchange='',
                          routing_key='addObject',
                          body=json.dumps(obj),
                          properties=pika.BasicProperties(
                            content_type='application/json',
                            content_encoding='utf-8',
                            delivery_mode = 2 # make message persistent
                        ))
    connection2.close()

def insert_face(k,imagefullname,image_id,x,y,w,h,encodings):
    objects_list=[]
    try:
        #generate small picture of the face
        image = cv2.imread(imagefullname)
        roi = image[y:y+h, x:x+w]
        dim = (96,96)
        resized = cv2.resize(roi, dim, interpolation = cv2.INTER_AREA)
        filename = "v2_{}_{}.png".format(image_id,k)
        cv2.imwrite("/pictures_work/facesv2/"+filename, resized)
        list = dlib_vect_to_array(encodings)
        obj = {
            "filefullname":imagefullname,
            "image_id":image_id,
            "x":x,
            "y":y,
            "w":w,
            "h":h,
            "description":"face",
            "confidence":1,
            "analyzer":analyzer,
            "analyzer_version":analyzer_version,
            "derived_from_object":None,
            "object_image_filename":filename,
            "face_encodings":list,
            "text_found":None
        }
        post_task(obj)
    except(Exception) as error:
        logger.error('Failed during face extraction', exc_info=True)



def extract_and_encode_face(ch, method, properties, body):
    obj = json.loads(body)
    f = obj['filefullname']
    image_id = obj['image_id']

    # Now process the image
    logger.debug("Processing image_id : {} file: {}".format(image_id,f))

    try:
        img = cv2.imread(f)#dlib.load_rgb_image(f)

        # Ask the detector to find the bounding boxes of each face. The 1 in the
        # second argument indicates that we should upsample the image 1 time. This
        # will make everything bigger and allow us to detect more faces.
        dets = detector(img, 1)
        logger.debug("Number of faces detected: {}".format(len(dets)))
        if (len(dets)==0):
            obj = {
                "filefullname":f,
                "image_id":image_id,
                "x":None,
                "y":None,
                "w":None,
                "h":None,
                "description":"no_face_found",
                "confidence":1,
                "analyzer":analyzer,
                "analyzer_version":analyzer_version,
                "derived_from_object":None,
                "object_image_filename":None,
                "face_encodings":None,
                "text_found":None
            }
            post_task(obj)

        # Now process each face we found.
        for k, d in enumerate(dets):
            logger.info("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format( k, d.left(), d.top(), d.right(), d.bottom()))
            # Get the landmarks/parts for the face in box d.
            shape = sp(img, d)
            # Compute the 128D vector that describes the face in img identified by
            # shape.  In general, if two face descriptor vectors have a Euclidean
            # distance between them less than 0.6 then they are from the same
            # person, otherwise they are from different people. Here we just print
            # the vector to the screen.
            #face_descriptor = facerec.compute_face_descriptor(img, shape)
            #print(face_descriptor)
            # It should also be noted that you can also call this function like this:
            #  face_descriptor = facerec.compute_face_descriptor(img, shape, 100, 0.25)
            # The version of the call without the 100 gets 99.13% accuracy on LFW
            # while the version with 100 gets 99.38%.  However, the 100 makes the
            # call 100x slower to execute, so choose whatever version you like.  To
            # explain a little, the 3rd argument tells the code how many times to
            # jitter/resample the image.  When you set it to 100 it executes the
            # face descriptor extraction 100 times on slightly modified versions of
            # the face and returns the average result.  You could also pick a more
            # middle value, such as 10, which is only 10x slower but still gets an
            # LFW accuracy of 99.3%.
            # 4th value (0.25) is padding around the face. If padding == 0 then the chip will
            # be closely cropped around the face. Setting larger padding values will result a looser cropping.
            # In particular, a padding of 0.5 would double the width of the cropped area, a value of 1.
            # would triple it, and so forth.

            # There is another overload of compute_face_descriptor that can take
            # as an input an aligned image.
            #
            # Note that it is important to generate the aligned image as
            # dlib.get_face_chip would do it i.e. the size must be 150x150,
            # centered and scaled.
            #
            # Here is a sample usage of that

            #print("Computing descriptor on aligned image ..")
            # Let's generate the aligned image using get_face_chip
            face_chip = dlib.get_face_chip(img, shape)
            #test saving thefacechip
            filename = "v2_{}_{}.png".format(image_id,k)
            cv2.imwrite("/pictures_work/faceschip/"+filename, face_chip)
            # Now we simply pass this chip (aligned image) to the api
            face_descriptor_from_prealigned_image = facerec.compute_face_descriptor(face_chip)

            left = d.left()
            if left < 0 :
                left = 0
            top = d.top()
            if top < 0 :
                top = 0

            insert_face(k,f,image_id,left,top, d.right()-d.left(), d.bottom()-d.top(),face_descriptor_from_prealigned_image)

    except (Exception) as error:
        logger.error('extract and encode failed', exc_info=True)



def receive(ch, method, properties, body):
    logger.debug("""rabbitmq receiver""")
    t = threading.Thread(target=extract_and_encode_face, args=(ch, method, properties, body,))
    t.daemon = True
    t.start()

    while t.is_alive():
        logger.debug("[INFO] heart beating")
        ch.connection.process_data_events()
        ch.connection.sleep(5)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    logger.debug("done")

def start():

    while(True):
        username = os.environ['RABBITMQ_USERNAME']
        pwd = os.environ['RABBITMQ_PWD']
        server = os.environ['RABBITMQ_SERVER']

        credentials = pika.PlainCredentials(username, pwd)
        parameters = pika.ConnectionParameters(server,
                                       5672,
                                       '/',
                                       credentials)
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue='extractFaces', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='extractFaces', on_message_callback=receive, auto_ack=False)
            logger.info(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        except (Exception) as error:
            logger.error('Rabbitmq connection failed', exc_info=True)
            time.sleep(5) 


if __name__ == '__main__':
    logger.info("starting face extraction consumption")

    #start server for API healthchecks.
    def server_start():
        app.run(debug=True, host="0.0.0.0", port=6000)
    p = multiprocessing.Process(target=server_start, args=())
    p.start()

    #start queue
    start();
    logger.info("done")
