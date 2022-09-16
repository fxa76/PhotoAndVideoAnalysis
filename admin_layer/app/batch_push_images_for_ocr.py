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
                WHERE (lower(fileextensions)='.jpg' or lower(fileextensions)='.png' or lower(fileextensions)='.jpeg'  or lower(fileextensions)='.tiff')
                and T1.image_id not in (
                    SELECT image_id FROM public.objects
	                WHERE analyzer = 'object_ocr' and analyzer_version = 100)
				   ORDER BY T1.creationdate DESC"""
    #reprocess images that had error o detection
    #sql = """SELECT T1.filefullname, T1.fileextensions,T1.image_id FROM public.images T1
    #              LEFT OUTER JOIN public.objects  T2
    #              ON (T1.filefullname = T2.filefullname)
    #              WHERE T2.description = 'error_on_detection' and T2.analyzer = 'face_detector_v2' and (fileextensions='.jpg' or fileextensions='.png' or fileextensions='.jpeg'  or fileextensions='.tiff')
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
    connection_queues.post_task(obj, "extractText");

def start():
    push_all_images_without()


if __name__ == '__main__':
    print(sys.argv)
    logger.info("staring to push image for OCR")
    start()
    logger.info("done")
