#!/usr/bin/python

# this program is made to be run incrementally (ie many times without destroying previous run)
# 1. load files one by one will update new files
import psycopg2

import argparse



#local imports
import connection_db
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--iterations", required=False,
    help="number of iteration of 10000 distances")
args = vars(ap.parse_args())



if __name__ == '__main__':
    logger.info("Starting to calculate face distances")
    iterations = args["iterations"]
    if iterations is None:
        iterations=1


    for i in range(int(iterations)):
        logger.info("Iteration {} / {}".format(i+1,iterations))

        try:
            # connect to the PostgreSQL server
            conn = connection_db.get_connection()
            cur = conn.cursor()
            try:
                cur.callproc('public.calculate_empty_distances',)
            except (Exception, psycopg2.DatabaseError) as error:
                logger.error("Procedure error {}".format(error), exc_info=True)
            cur.close()
            conn.commit()
            conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error("Error {}".format(error), exc_info=True)
