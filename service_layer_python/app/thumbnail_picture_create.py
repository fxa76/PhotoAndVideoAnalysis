#!/usr/bin/env python
import cv2
import base64

#local imports
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

def get_image_base_64(img):
    image_base64 = "data:image/jpg;base64,"
    try:
        retval, buffer = cv2.imencode('.jpg', img)
        image_base64 += base64.b64encode(buffer).decode('utf-8').replace('\n', '')
    except(Exception) as error:
        logger.error("Error encoding get_image_base_64 : {}".format(error))
        logger.error('Failed to convert image to base 64', exc_info=True)

    return image_base64

def get_thumbnail(filefullname):
    try:
        img = cv2.imread(filefullname, 1)
        try:
            #rescale img to height 700
            max_h=100
            height, width, depth = img.shape
            img_scale = max_h/height
            new_w,new_h = width*img_scale, height*img_scale
            img_small = cv2.resize(img,(int(new_w),int(new_h)))
            image_base64 = get_image_base_64(img_small)
            return image_base64
        except (Exception) as error:
            logger.error("Error encoding small image get_base_64_small : {}".format(error))
            logger.error('Failed to convert image to small image base 64', exc_info=True)
        return "error when converting image"

    except (Exception) as error:
        logger.error("Error reading file")
