import psycopg2
import connection_db

#local imports
import logging.config
import file_calculate_sha

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

def update(image_id,sha512):
    sql = """UPDATE images set sha512 = %s WHERE image_id = %s"""

    try:
        # connect to the PostgreSQL server
        conn = connection_db.get_connection()
        cur = conn.cursor()
        cur.execute(sql,(sha512,image_id,))

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error('Failed updating image sha512', exc_info=True)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def iterate_thru_images():
    #iterate thru images that have not yet been analyzed
    sql = """SELECT filefullname, image_id FROM public.images
            where sha512 is null;"""
    try:
        # connect to the PostgreSQL server
        conn = connection_db.get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            logger.debug("Processing row : {}".format(row))
            filefullname = row[0]
            image_id = row[1]
            update(image_id,file_calculate_sha.calculate_hash(filefullname))
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error('Failed while iterating thru images', exc_info=True)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    iterate_thru_images()
    logger.info("done")
