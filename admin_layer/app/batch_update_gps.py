import psycopg2

#local imports
import connection_db
import exif_extract_gps_coord

import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

def iterate_thru_images():
    sqlquery = "SELECT image_id, filefullname FROM public.images where ((lat is null or lon is null) and (fileextensions = '.jpeg' or fileextensions='.jpg') and (coord_from_exif is null) ) order by creationdate desc"
    #OFFSET 0 FETCH NEXT 10 ROWS ONLY;
    conn = connection_db.get_connection()
    cur = conn.cursor()
    cur.execute(sqlquery)

    try:
      while True:
        row = cur.fetchone()
        if cur.rowcount == 0 :
            logger.debug("no image fits quiery")
            break;
        else :
            image_id = row[0]
            imagefullname = row[1]
            logger.debug("Extracting gps coord from {}".format(imagefullname))
            try:
                lat = None
                lon = None
                coord_from_exif = False

                lat,lon,coord_from_exif = exif_extract_gps_coord.get_gps_coord(imagefullname)

                logger.debug("to be inserted image_id {} , lat {}, lon {}".format(image_id,lat,lon))
                sql = """Update public.images set lat = %s, lon=%s,coord_from_exif=%s
                   Where image_id = '%s'"""
                try:
                  cur2 = conn.cursor()
                  cur2.execute(sql,( lat,lon,coord_from_exif,image_id))
                  count = cur2.rowcount
                  logger.debug(count, "Record Updated successfully ")
                  cur2.close()
                  logger.debug("insert done")
                except(Exception)as error:
                  logger.error( error)
                  if cur2 is not None:
                    cur2.close()
            except(Exception)as error:
              logger.error( error)


    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    finally:
        if cur is not None:
            cur
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    logger.debug("starting extracting gps coordinates")
    iterate_thru_images()
    logger.debug("done")
