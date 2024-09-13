import pandas as pd
import io
from geopy.geocoders import Nominatim
import psycopg2
import logging.config

geolocator = Nominatim(user_agent="PhotoAndVideoAnlysis")

# local imports
import connection_db

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)


def iterate_thru_images():
    sqlquery = """SELECT image_id , lat, lon
    FROM public.images
    WHERE (
        lon is not null
        AND
        lat is not null
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
            lat = float(row[1])
            lon = float(row[2])
            address = None
            try:
                location = geolocator.reverse("{}, {}".format(lat, lon), exactly_one=True)
                address = location.raw['address']
                logger.debug("address{}".format(address))
            except(Exception) as error:
                logger.error(
                    "Error while getting address for for image id {} : {}".format(image_id, error))

            sql = """UPDATE public.images
                SET address = %s,country = %s
                WHERE image_id = '%s'"""
            try:
                cur2 = conn.cursor()
                cur2.execute(sql, (address['road'],address['country'], image_id,))
                cur2.close()
                logger.debug("{}/{}".format(image_id,address['country']))
                logger.debug("insert done")
            except(Exception) as error:
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
