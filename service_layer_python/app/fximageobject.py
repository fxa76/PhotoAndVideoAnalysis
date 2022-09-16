import fximageutils
import cv2


class FXImageObject(object):
    def __init__(self,objects_id, filefullname, bbox, description, confidence, analyzer, analyzer_version, x, y, w, h,image_id,derived_from_object,object_image_filename,face_id,text_found):
        self.objects_id = objects_id
        self.filefullname = filefullname
        self.bbox = bbox
        self.description = description
        self.confidence = confidence
        self.analyzer = analyzer
        self.analyzer_version = analyzer_version
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image_id = image_id
        self.derived_from_object = derived_from_object
        self.object_image_filename = object_image_filename
        self.face_id = face_id
        self.text_found = text_found
