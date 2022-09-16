#!/usr/bin/env python

# USAGE
# python face_export.py -f1
#
# PURPOSE
# export (copy) all facechips to one directory

# import the necessary packages
import argparse
import shutil
import logging.config
#local imports
import connection_db



logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--faceId", required=True,
    help="give face id to e exported")
args = vars(ap.parse_args())

logger.info("Gettings files...")

sqlquery = """SELECT object_image_filename,face_id
FROM public.objects
WHERE description = 'face'
    AND face_id = %s"""


conn = connection_db.get_connection()
conn.autocommit = True
cur = conn.cursor()
id_str = "{}".format(args["faceId"])
print("ID is {}".format(id_str))
cur.execute(sqlquery,(id_str,) )
rows = cur.fetchall()
data = []
for row in rows :
    source = "{}/{}".format("/pictures_work/faceschip",row[0])
    destination = "{}/{}".format("/pictures_work/export",row[0])
    dest = shutil.copy(source, destination)
    logger.info("{}=>{}".format(source, destination))
cur.close()
conn.close()
