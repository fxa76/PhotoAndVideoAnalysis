#!/usr/bin/python

from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS
from PIL import Image


#local imports
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

def get_model(imagefullname):
    logger.debug("getting model for image : {}".format(imagefullname))

    exif = get_exif(imagefullname)
    model = None
    if (exif!=None):
        exif_obj = get_exif_data_obj(exif)
        if(exif_obj!=None and 'Model' in exif_obj):
            model = exif_obj['Model']
            #line below is required to prevent : Insert Error : A string literal cannot contain NUL (0x00) characters.
            if (model!=None):
                model = model.split('\0',1)[0]
    return model


def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_exif_data_obj(exif):
    exif_data = {}
    for (tag, value) in exif.items():
        decoded_tag = TAGS.get(tag, tag)
        exif_data[decoded_tag] = value
    return exif_data
