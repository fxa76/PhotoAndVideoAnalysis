import sys

import os
import platform
import cvlib as cv
from cvlib.object_detection import draw_bbox
import cv2
import json
import pika
import logging.config

files=['/pictures/test/test.jpeg']

for f in files :
    image = cv2.imread(f)
    # apply object detection
    bbox, label, conf = cv.detect_common_objects(image)
    print("bbox: {} label : {} confidence : {}".format(bbox, label, conf))
