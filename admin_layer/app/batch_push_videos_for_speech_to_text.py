#!/usr/bin/python
import sys
import os
import argparse
import psycopg2
import json
import pika

#local imports
import connection_db
import connection_queues
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


def push_all_images_without():
    #iterate thru images that have not yet been analyzed
    sql = """SELECT T1.filefullname, T1.fileextensions,T1.image_id,T1.creationdate FROM public.images as T1
                WHERE (lower(fileextensions)='.mp4' or lower(fileextensions)='.mov' or lower(fileextensions)='.avi')
                and T1.image_id not in (select image_id FROM public.objects
	               where analyzer = 'video_speech_to_text' and analyzer_version = 100)
				   order by T1.creationdate desc"""
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
            push_image(image_id,filefullname)
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
    connection_queues.post_task(obj, "extractSpeech");

def start():
    push_all_images_without()


if __name__ == '__main__':
    print(sys.argv)
    logger.info("staring to push video for speech to text")
    start()
    logger.info("done")
