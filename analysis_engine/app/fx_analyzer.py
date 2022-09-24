import os
from threading import Timer
import logging.config
import logging

from detectedobject import DetectedObject

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

analyzer_name = 'analysis_template'
analyzer_version = 100


def perform_task(image_id) -> []:
    logger.debug("performing task")

    #Obj 1
    obj1 = DetectedObject()
    obj1.analyzer = analyzer_name
    obj1.analyzer_version = analyzer_version
    obj1.description = "not implemented analysis 2"
    obj1.image_id = image_id

    obj_arr_task = [ obj1]

    return obj_arr_task
