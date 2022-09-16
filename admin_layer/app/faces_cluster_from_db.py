#!/usr/bin/env python

# USAGE
# python faces_cluster_from_db.py --iteration 1
#
#PURPOSE
# add a face_id to a face in the db.
# iteration is used to iteratively improve identification.
# run the first iteration manually with line 69 eps set to 34 and smaples to 20
# then  UPDATE objects set face_id = null, face_id_iteration = null where face_id = -1

# import the necessary packages
from sklearn.cluster import DBSCAN
from sklearn import metrics
from imutils import build_montages
import numpy as np
import argparse
import pickle
import cv2
import os
from shutil import copyfile
import ntpath
import logging.config
#local imports
import connection_db

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--iteration", required=True,
    help="give an iteration number")
args = vars(ap.parse_args())

logger.info("loading encodings...")

sqlquery = """SELECT objects_id, description, face_encodings,object_image_filename,face_id
FROM public.objects
WHERE description = 'face'
    AND analyzer_version = 200
    AND face_encodings is not null"""
    #AND face_id is null


conn = connection_db.get_connection()
conn.autocommit = True
cur = conn.cursor()
cur.execute(sqlquery)
rows = cur.fetchall()
data=[]
for row in rows :
    obj={}
    obj['objects_id'] = row[0]
    obj['encodings'] = row[2]
    # filepath = "{}/{}".format("/pictures_work/faces",row[3])
    # obj['filepath'] =filepath
    # logger.debug(filepath)
    data.append(obj)
cur.close()


# load the serialized face encodings + bounding box locations from
# disk, then extract the set of encodings to so we can cluster on
# them
data = np.array(data)
encodings = [d["encodings"] for d in data]

# cluster the embeddings
logger.info("clustering...")
#clt = DBSCAN(metric="euclidean", n_jobs=args["jobs"])
#clt = DBSCAN(eps=0.35, min_samples=20,metric="euclidean")
clt = DBSCAN(eps=0.35, min_samples=20,metric="euclidean")
clt.fit(encodings)


# determine the total number of unique faces found in the dataset
labelIDs = np.unique(clt.labels_)
numUniqueFaces = len(np.where(labelIDs > -1)[0])
logger.info("# unique faces: {}".format(numUniqueFaces))



# loop over the unique face integers
for labelID in labelIDs:
    # find all indexes into the `data` array that belong to the
    # current label ID, then randomly sample a maximum of 100 indexes
    # from the set
    logger.info("faces for face ID: {}".format(labelID))
    idxs = np.where(clt.labels_ == labelID)[0]

    # initialize the list of faces to update the db with face_id
    faces = []
    face_id = labelID.item()
    face_id_iteration = args["iteration"]

    sql = """INSERT INTO public.face_id
    (face_id, face_id_iteration, hidden)
	VALUES (%s, %s, false);"""
    try:
      cur3 = conn.cursor()
      cur3.execute(sql,( face_id,face_id_iteration,))
      cur3.close()
    except(Exception)as error:
        logger.error('Failed to insert info in db', exc_info=True)
    finally:
      if cur3 is not None:
        cur3.close()

    # loop over the sampled indexes
    for i in idxs:
        # logger.debug(data[i]["filepath"])
        #faces.append(data[i])
        faces.append([face_id,face_id_iteration,data[i]["objects_id"]])

    sql = """UPDATE objects SET face_id = %s, face_id_iteration=%s
       WHERE objects_id = '%s'"""
    try:
      cur2 = conn.cursor()
      cur2.executemany(sql,faces)#( face_id,face_id_iteration,data[i]["objects_id"],)
      cur2.close()
    except(Exception)as error:
        logger.error('Failed to insert info in db', exc_info=True)
    finally:
      if cur2 is not None:
        cur2.close()

    logger.debug("number of faces found : {}".format(len(faces)))

conn.close()
