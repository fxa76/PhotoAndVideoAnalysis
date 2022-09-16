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
import psycopg2
import json
import pika
import argparse

#local imports
import connection_db
import connection_queues
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

def push_all_images_without():
    #iterate thru images that have not yet been analyzed
    sql = """SELECT T1.filefullname, T1.fileextensions,T1.image_id FROM public.images T1
                LEFT OUTER JOIN public.objects  T2
                ON (T1.filefullname = T2.filefullname)
                WHERE T2.filefullname IS NULL and  (fileextensions='.jpg' or fileextensions='.png' or fileextensions='.jpeg'  or fileextensions='.tiff')"""
    #reprocess images that had nothin_found
    #sql = """SELECT T1.filefullname, T1.fileextensions,T1.image_id FROM public.images T1
    #             LEFT OUTER JOIN public.objects  T2
    #              ON (T1.filefullname = T2.filefullname)
    #        WHERE T2.description = 'nothing_found'  and (fileextensions='.jpg' or fileextensions='.png' or fileextensions='.jpeg'  or fileextensions='.tiff')
    #              """
    try:
        # connect to the PostgreSQL server
        conn = connection_db.get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            logger.debug("Processing row : {}".format(row))
            filefullname = row[0]
            image_id = row[2]
            push_image(image_id, filefullname)
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error('Failed while iterating thru images', exc_info=True)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def push_image_by_id(image_id):
    sql = """SELECT filefullname FROM public.images 
                   WHERE image_id = %s"""

    try:
        # connect to the PostgreSQL server
        conn = connection_db.get_connection()
        cur = conn.cursor()
        cur.execute(sql,(image_id,))
        while True:
            row = cur.fetchone()
            if row == None:
                break
            logger.debug("Processing row : {}".format(row))
            filefullname = row[0]
            push_image(image_id, filefullname)
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error('Failed while iterating thru images', exc_info=True)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def push_image(image_id,filefullname):
    obj = {"image_id": image_id, "filefullname": filefullname}
    connection_queues.post_task(obj, "extractObjects");

def start():
    push_all_images_without()

if __name__ == '__main__':
    print(sys.argv)
    logger.info("staring to push image for objects detetection")
    ap = argparse.ArgumentParser()


    ap.add_argument("-a", "--action", required=True, choices=['batch','single'],help="Push all images with no objects or a single image by Id")

    # sub parser for Clean
    ap.add_argument("-i", "--image_id", required='single' in sys.argv, help="ID of image to be pushed")
    args = vars(ap.parse_args())
    if (args["action"]=="batch"):
        start();
    else:
        push_image_by_id(args["image_id"])

    logger.info("done")
