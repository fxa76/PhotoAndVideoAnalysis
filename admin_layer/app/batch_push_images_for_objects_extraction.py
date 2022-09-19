#!/usr/bin/python

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
