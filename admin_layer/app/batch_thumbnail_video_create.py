import cv2
import base64
import psycopg2
#local imports
import connection_db
import logging.config
import thumbnail_video_create

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

def iterate_thru_images():
    sqlquery = """SELECT image_id, filefullname
    FROM public.images
    WHERE (
        (
        lower(fileextensions) in  ('.mov','.mp4','.mpg','.avi','.3gp'))
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

        img = thumbnail_video_create.get_thumbnail(imagefullname)

        sql = """UPDATE public.images
            SET thumbnail = %s
           WHERE image_id = '%s'"""
        try:
          cur2 = conn.cursor()
          cur2.execute(sql,(img, image_id, ))
          #count = cur2.rowcount
          #print(count, "Record Updated successfully ")
          cur2.close()
          logger.debug("insert done {}".format(image_id))
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
    logger.debug("starting video thumbnail creation")
    iterate_thru_images()
    logger.debug("video thumbnail creation done")
