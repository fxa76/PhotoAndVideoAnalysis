import os
import argparse
import sys
import datetime
import shutil
import logging.config
import psycopg2

#local imports
import connection_db

logging.config.fileConfig('duplicate_finder_logging.conf')
logger = logging.getLogger(__name__)

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True, help="Base directory to analyse")

args = vars(ap.parse_args())


def get_files_on_disk(basedirectory):
    j=0
    files_on_disk =[]
    acceptable_extensions = ['png','tiff','jpg','jpeg']
    for root, dirs, files in os.walk(basedirectory, topdown = False):
        for name in files:
            files_on_disk.append(name)

    return files_on_disk

def get_files_in_db():
    sqlquery = """SELECT objects_id, description, face_encodings,object_image_filename,image_id,face_id
    FROM public.objects
    WHERE description = 'face'
        AND analyzer_version = 200
        """
    conn = connection_db.get_connection()
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(sqlquery)
    rows = cur.fetchall()
    data=[]
    for row in rows :
        obj={}
        obj['objects_id'] = row[0]
        obj['filename'] = row[3]
        obj['image_id'] = row[4]
        data.append(obj)
    cur.close()
    conn.close()
    return data

def delete_obj(list_image_ids):
    sqlquery = """DELETE FROM public.objects
    WHERE description = 'face'
        AND analyzer_version = 200
        AND image_id in %(image_id_list)s
        """
    conn = connection_db.get_connection()
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(sqlquery,{
        'image_id_list':tuple(list_image_ids),
        })
    rows = cur.fetchall()
    logger.info("will delete {} rows".format(len(rows)))
    cur.close()
    conn.close()

if __name__ == '__main__':
    a = datetime.datetime.now()
    source_dir = args["directory"]
    logger.info("starting analysis of directory {}".format(source_dir))
    files_on_disk= get_files_on_disk(source_dir)
    logger.info("Fetching all face objects".format(source_dir))
    files_in_db = get_files_in_db()
    logger.info("start checking {} files in db against {} files on disk".format(len(files_in_db), len(files_on_disk)))
    images_to_reprocess=[]
    cpt=0
    for obj in files_in_db :
        if (obj['filename'] not in files_on_disk ):
            logger.info("Missing file {} on disk for object id {} for image id {}".format(obj['filename'],obj['objects_id'],obj['image_id']))
            cpt=cpt+1
            if(obj['image_id'] not in images_to_reprocess):
                images_to_reprocess.append(obj['image_id'])

    logger.info("found {} images to reprocess for {} faces missing".format(len(images_to_reprocess),cpt))
    delete_obj(images_to_reprocess)

    b = datetime.datetime.now()
    c = b - a
    logger.info("Time taken : {}s OR {}ms".format(c.seconds,c.microseconds))
