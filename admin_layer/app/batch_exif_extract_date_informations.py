from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS
from PIL import Image

import datetime
import platform
import os

#local imports
import connection_db
import psycopg2
import logging.config
import exif_extract_date_informations

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


def iterate_thru_images():
    sqlquery = """SELECT image_id, filefullname
    FROM public.images
    WHERE (
        (lower(fileextensions) = '.jpeg' or lower(fileextensions)='.jpg')

        )
    ORDER BY creationdate DESC"""
    conn = connection_db.get_connection()
    cur = conn.cursor()
    cur.execute(sqlquery)

    try:
      while True:
        row = cur.fetchone()
        if row == None:
            break
        image_id = row[0]
        imagefullname = row[1]

        date, epoch = exif_extract_date_informations.get_date(imagefullname)

        sql = """UPDATE public.images
            SET timestamp = %s, creationdate = %s
           WHERE image_id = '%s'"""
        try:
          cur2 = conn.cursor()
          cur2.execute(sql,(date, epoch,image_id, ))
          cur2.close()
          logger.debug("insert done")
        except(Exception)as error:
          logger.error("Insert Error : {}".format(error))
          if cur2 is not None:
            cur2.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if cur is not None:
            cur
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    iterate_thru_images()
    logger.debug("done")
