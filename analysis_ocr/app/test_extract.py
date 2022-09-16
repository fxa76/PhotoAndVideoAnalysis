import json
import logging.config
import time

import cv2
import pika
import pytesseract
from pytesseract import Output

analyzer = 'object_ocr'
analyzer_version = 100



filefullname = '/pictures/3DPrint/2020_profile__64148.1479159935.jpg'
image_id='test'
print("analyzing image : {} {}".format(image_id, filefullname))
im = cv2.imread(filefullname, cv2.IMREAD_COLOR)
rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
# Run tesseract OCR on image
h, w, c = rgb.shape
d = pytesseract.image_to_data(rgb, output_type=Output.DICT)
n_boxes = len(d['text'])

print(n_boxes)

if n_boxes == 0:
    obj_task = {
        "filefullname": filefullname,
        "image_id": image_id,
        "x": 0,
        "y": 0,
        "w": 0,
        "h": 0,
        "description": "no_text_found",
        "confidence": 1,
        "analyzer": analyzer,
        "analyzer_version": analyzer_version,
        "derived_from_object": None,
        "object_image_filename": None,
        "face_encodings": None,
        "text_found": None
    }
    print("Pushed OBJ {}".format(obj_task))
else:
    for i in range(n_boxes):
        if len(d['text'][i].replace(' ', '')) > 0:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])

            obj_task = {
                "filefullname": filefullname,
                "image_id": image_id,
                "x": x,
                "y": y,
                "w": w,
                "h": h,
                "description": "text_found",
                "confidence": d['conf'][i],
                "analyzer": analyzer,
                "analyzer_version": analyzer_version,
                "derived_from_object": None,
                "object_image_filename": None,
                "face_encodings": None,
                "text_found": d['text'][i]
            }
            print("Pushed OBJ {}".format(obj_task))
