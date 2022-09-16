#!/usr/bin/env python

# USAGE
# python faces_cluster_from_db.py --iteration 1
#
# PURPOSE
# add a face_id to a face in the db.
# iteration is used to iteratively improve identification.
# run the first iteration manually with line 69 eps set to 34 and smaples to 20
# then  UPDATE objects set face_id = null, face_id_iteration = null where face_id = -1

# import the necessary packages
import numpy as np
import pandas as pd
import logging.config
from scipy.spatial.distance import pdist
from sklearn.metrics.pairwise import pairwise_distances
# local imports
import fxconnection
import thumbnail_picture_create
import time

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

def get_similar_to_id(face_id:object):
    logger.info("loading encodings...")
    # load the serialized face encodings

    sqlquery = """SELECT objects_id, description, face_encodings,object_image_filename,face_id,image_id
    FROM public.objects
    WHERE description = 'face'
    AND analyzer_version = 200
    AND face_encodings is not null"""
    # FETCH first 100 rows only"""


    conn = fxconnection.get_connection()
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(sqlquery)
    rows = cur.fetchall()

    fetch_size = len(rows)

    arr_obj_id = np.empty((fetch_size,),np.int64)
    arrX = np.empty((fetch_size,128),np.float64)
    arr_filenames = np.empty((fetch_size,),object)
    arr_img_id = np.empty((fetch_size,), np.int64)

    i=0
    for row in rows:
        arr_obj_id[i] = row[0]
        arrX[i] = row[2]
        arr_filenames[i] = row[3]
        arr_img_id[i] = row[5]
        i+=1

    cur.close()
    conn.close()

    logger.info("np array creation")

    start_time = time.time()

    df2 = pairwise_distances(arrX,metric='euclidean')

    print("T1 --- %s seconds ---" % (time.time() - start_time))
    # add index and columns names
    df3 = pd.DataFrame(data=df2,index=arr_obj_id,columns=arr_obj_id)
    logger.info(df3)

    logger.info("getting subset")
    # set reference image by filename
    reference_image = np.int64(face_id)
    print("reference image is {}".format(reference_image))
    logger.info(type(reference_image))
    logger.info(type(df3.index[0]))
    if reference_image in df3.index:
        # extract all lines only 1 column
        first_image=df3[[reference_image]]

        # limit to distance below threshold
        first_image_v2=first_image[first_image[reference_image]<0.5]

        print(first_image_v2)

        first_image_v2.sort_values(by=reference_image, axis=0, ascending=True, inplace=True)

        objs = []
        for index, row in first_image_v2.iterrows():

            result = np.where(arr_obj_id == index)
            filename = arr_filenames[result[0][0]]
            image_path = "/pictures_work/faceschip/{}".format(filename)
            image_id = arr_img_id[result[0][0]]
            obj = {
                'objects_id' : index,
                'distance' : "{:.4f}".format(row.iloc[0]),
                'image_id' : str(image_id),
                'image' : thumbnail_picture_create.get_thumbnail(image_path)

            }
            objs.append(obj)

        # logger.info(objs)
        return objs
    else:
        return "not a valid index"

