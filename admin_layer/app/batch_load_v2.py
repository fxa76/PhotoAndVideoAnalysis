#!/usr/bin/python

# this program is made to be run incrementally (ie many times without destroying previous run)
# 1. load files one by one will update new files

import psycopg2
import os
import platform
import base64
import cv2
import argparse
import sys
import shutil

import connection_queues

#local imports
import connection_db
import file_calculate_sha
import logging.config

import exif_extract_date_informations
import exif_extract_gps_coord
import exif_extract_model_informations
import exif_date_in_video

import thumbnail_video_create
import thumbnail_picture_create
import thumbnail_raw_create

import file_duplicates_finder
import file_move
import files_on_disk
import file_check_if_already_in_db

import batch_push_images_for_objects_extraction
import batch_push_images_for_face_extraction

logging.config.fileConfig('logging.conf')
logger = logging.getLogger("main")

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--source", required=False,
    help="name of the origine of images to be loaded")
args = vars(ap.parse_args())

def add_file(f,source):
        logger.info("reading info for file {}".format(f))
        filefullname = f
        extension_dot_position = filefullname.rfind('.')
        extension = filefullname[extension_dot_position:].lower()
        size = os.path.getsize(filefullname)
        name = os.path.basename(filefullname)
        root = os.path.dirname(filefullname)

        thumbnail = None
        date = None
        epoch= None
        lat = None
        lon = None
        coord_from_exif = None
        model = None

        #thumbnail creation and date extractions differs for video and images.
        if extension in ['.jpg','.png','.jpeg','.tiff','.webp']:
            thumbnail = thumbnail_picture_create.get_thumbnail(filefullname)
            date, epoch = exif_extract_date_informations.get_date(filefullname)
            #Exif data
            if extension in ['.jpg','.jpeg','.tiff']:
                lat, lon, coord_from_exif = exif_extract_gps_coord.get_gps_coord(filefullname)
                model = exif_extract_model_informations.get_model(filefullname)
        elif extension in ['.mp4','.mov','.mpg','.avi','.3gp','.webm']:
            thumbnail = thumbnail_video_create.get_thumbnail(filefullname)
            date, epoch,src = exif_date_in_video.get_mov_timestamps(filefullname)
        elif extension in ['.orf','.raw']:
            thumbnail = thumbnail_raw_create.get_thumbnail(filefullname)
            date, epoch = exif_extract_date_informations.get_date(filefullname)
        load_one_image([filefullname,name,root,extension,size,date,epoch,source,thumbnail,file_calculate_sha.calculate_hash(filefullname),model,lat, lon, coord_from_exif ])


def load_one_image(data):
    #insert the new files
    sql = "INSERT INTO images(filefullname,filename,filepath,fileextensions,filesize,timestamp,creationdate,source,thumbnail,sha512,model,lat, lon, coord_from_exif) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING image_id"
    try:
        # connect to the PostgreSQL server
        conn = connection_db.get_connection()
        cur = conn.cursor()
        try:
            #logger.debug("inserting file with data {}".format(file))
            cur.execute(sql,data)
            image_id = cur.fetchone()[0]
            logger.info("image inserted with id : {}".format(image_id))

            obj= {"image_id":image_id,"filefullname":data[0]};

            connection_queues.post_task(obj,"extractObjects");
            connection_queues.post_task(obj,"extractFaces");

        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error,exc_info=True)
            logger.error(sql)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("Error in load_one_by_one_images Insert statement ", exc_info=True)

    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    logger.info("Starting to load images")
    source = args["source"]
    if source is None:
        source=""

    source_dir = '/pictures_inbox'
    target_dir = '/pictures'
    recycle_dir = '/pictures_work/duplicates'
    logger.info("I will FIRST get files in directory {} ".format(source_dir))

    src_files = files_on_disk.get_files_on_disk(source_dir)
    logger.debug("Files in source directory : {}".format(len(src_files)))

    for f in src_files:
        if (file_check_if_already_in_db.file_already_in_db(f)):
            #Bounce file
            file_move.move_file_hierarchy(source_dir,recycle_dir,f)
            logger.debug("moving file recycle :{}".format(f))
        else:
            #Add file
            logger.debug("Adding file in db :{}".format(f))
            target = file_move.move_file_hierarchy(source_dir,target_dir,f)
            add_file(target,source)


    logger.info("done")
