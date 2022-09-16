#!/usr/bin/python

from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS
from PIL import Image


#local imports
import connection_db
import psycopg2
import exif_extract_model_informations
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


def iterate_thru_images():
    sqlquery = """SELECT image_id, filefullname
    FROM public.images
    WHERE (
        (fileextensions = '.jpeg' or fileextensions='.jpg')
        AND model is null
        )
    ORDER BY creationdate DESC"""
    conn = connection_db.get_connection()
    cur = conn.cursor()
    cur.execute(sqlquery)

    try:
      while True:
        row = cur.fetchone()
        if row == None:
            logger.debug("no image fits quiery")
            break
        image_id = row[0]
        imagefullname = row[1]
        model="unknwon"
        try:
            logger.debug("getting model for image : {}".format(imagefullname))

            model = exif_extract_model_informations.get_model(imagefullname)
        except (Exception) as error:
            logger.error("exif data error")
            logger.error(error)

        sql = """UPDATE public.images
            SET model = %s
           WHERE image_id = '%s'"""
        try:
          cur2 = conn.cursor()
          cur2.execute(sql,(model,image_id, ))
          #count = cur2.rowcount
          #print(count, "Record Updated successfully ")
          cur2.close()
          logger.debug("insert done")
        except(Exception)as error:
          logger.error("Insert Error : {}".format(error))
          if cur2 is not None:
            cur2.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    finally:
        if cur is not None:
            cur
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    iterate_thru_images()
    logger.debug("done")
