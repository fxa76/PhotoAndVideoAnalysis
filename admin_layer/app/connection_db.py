#!/usr/bin/env python
import psycopg2
import os

import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


def get_connection():
    try:
        user_name = os.environ['POSTGRES_USER']
        password = os.environ['POSTGRES_PASSWORD']
        db_name = os.environ['POSTGRES_DB']
        host = os.environ['POSTGRES_HOST']
        port = os.environ['POSTGRES_PORT']

        logger.info("password is {}".format(password))
    except(KeyError) as error:
        logger.error("Fatal error : can't find environment variable to access the database : {}".format(error))
        exit(1)

    conn = psycopg2.connect(
              dbname=db_name,
              user=user_name,
              host=host,
              port = port,
              password=password
            )
    conn.autocommit = True
    return conn
