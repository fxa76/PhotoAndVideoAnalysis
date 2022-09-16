#!/usr/bin/python

# this program is made to be run incrementally (ie many times without destroying previous run)
# 1. load files one by one will update new files
import psycopg2

import argparse
import sys
import os

#local imports
import connection_db
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)



def delete_objects_from_db_by_image_id(image_id):
    #get face chip files
    sql = """SELECT object_image_filename FROM objects
        WHERE image_id = %s and description='face'"""
    try:
        # connect to the PostgresSQL server
        conn = connection_db.get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql,(image_id,))
            records = cur.fetchall()
            for row in records :
                filename = row[0]
                logger.debug("images deleted : {}".format(filename))
                try:
                    os.remove("/pictures_work/faceschip/{}".format(filename))
                except OSError as file_error:
                    logger.error("delete file error {}".format(file_error), exc_info=True)
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error("Select error {}".format(error),exc_info=True)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("Error in load_one_by_one_images Delete statement for Objects ", exc_info=True)

    #delete objects from database
    sql = """DELETE FROM objects
    WHERE image_id = %s"""
    try:
        # connect to the PostgresSQL server
        conn = connection_db.get_connection()
        cur = conn.cursor()
        try:
            cur.execute(sql,(image_id,))
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error("deletion error {}".format(error), exc_info=True)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("Error in load_one_by_one_images Delete statement for Objects ", exc_info=True)

    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    logger.info("starting Objects Db Access")
    parser = argparse.ArgumentParser(description='Access to objects in DB')
    parser.add_argument("-id", "--image_id", required=True, help="image id for objects")
    args = vars(parser.parse_args())
    image_id = args["image_id"]
    delete_objects_from_db_by_image_id(image_id)
    logger.info("done")
