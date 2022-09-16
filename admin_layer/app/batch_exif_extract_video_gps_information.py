from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS
from PIL import Image

import datetime
import platform
import os

# local imports
import connection_db
import psycopg2
import logging.config
import exif_gps as egps
import exifread
import ffmpeg
import re 

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


def get_gps_coordinates_from_mov(filepath):
    input = ffmpeg.probe(filepath)
    print(input)
    str = input['format']['tags']['com.apple.quicktime.location.ISO6709']
    pattern = "[\+\-]\d*[.,]\d*"
    matches = re.findall(pattern, str)
    if len(matches) == 3:
        lat = matches[0]
        lon = matches[1]
    
    return lat, lon



def iterate_thru_images():
    sqlquery = """SELECT image_id, filefullname
    FROM public.images
    WHERE (
        (lower(fileextensions) = '.mov')
        AND
        lat is null
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

            lat = None
            lon = None
            coord_from_exif = False
            try:
                with open(imagefullname, 'rb') as image_file:
                    lat, lon = get_gps_coordinates_from_mov(imagefullname)
                    coord_from_exif = True

            except(Exception)as error:
                logger.error("Error while getting gps info for image id {} file {}: {}".format(image_id,imagefullname,error))

            sql = """UPDATE public.images
                SET lat = %s, lon = %s, coord_from_exif=%s
                WHERE image_id = '%s'"""
            try:
                cur2 = conn.cursor()
                cur2.execute(sql, (lat, lon, coord_from_exif, image_id,))
                cur2.close()
                logger.debug("{}/{}/{}/{}/{}".format(imagefullname,lat, lon, coord_from_exif, image_id))
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
