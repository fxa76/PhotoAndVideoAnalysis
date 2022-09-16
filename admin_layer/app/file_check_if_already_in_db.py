#!/usr/bin/env python
import psycopg2
import argparse

#local imports
import file_calculate_sha
import logging.config
logging.config.fileConfig('duplicate_finder_logging.conf')
logger = logging.getLogger(__name__)
import connection_db

def file_already_in_db(filefullname):
    sha512 = file_calculate_sha.calculate_hash(filefullname)
    #insert the new files
    sql = "SELECT * FROM images WHERE sha512=%s"
    try:
        # connect to the PostgreSQL server
        conn = connection_db.get_connection()
        cur = conn.cursor()
        logger.debug("checking if file {} with sha512 {} exists in db".format(filefullname,sha512))
        cur.execute(sql,(sha512,))
        if cur.rowcount > 0 :
            logger.debug("File already exist")
            return True
        else:
            logger.debug("File doesn't exist in DB")
            return False
    except(Exception) as error:
        print(error)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--file", required=True, help="path to file to be checked")
    args = vars(ap.parse_args())
    filefullname=args['file']
    file_exists , error = file_already_in_db(filefullname)
    logger.debug("file exists is: {}".format(file_exists))
