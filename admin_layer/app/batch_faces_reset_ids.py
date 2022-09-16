#!/usr/bin/env python
import argparse
import datetime
import psycopg2

#local imports
import connection_db
import logging.config

#get args

#setup logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

def reset():
    try:
        sql1="UPDATE public.objects SET face_id=null, face_id_iteration=null"
        sql2="TRUNCATE table public.face_id"
        # connect to the PostgreSQL server
        conn = connection_db.get_connection()
        cur = conn.cursor()
        cur.execute(sql1)
        cur.execute(sql2)

        cur.close()
    except (psycopg2.DatabaseError) as error:
        logger.error("error " , exc_info=True)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    logger.info("starting")
    start = datetime.datetime.now()
    reset()
    end = datetime.datetime.now()
    time_taken = end - start
    logger.info("Done, time taken : {}s OR {}ms".format(time_taken.seconds,time_taken.microseconds))
