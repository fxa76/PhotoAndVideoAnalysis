from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS
from PIL import Image

import datetime
import platform
import os

#local imports
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getmtime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def get_date(imagefullname):
    date= None
    epoch = None
    try:
        date = Image.open(imagefullname)._getexif()[36867]
        #line below is required to prevent : Insert Error : A string literal cannot contain NUL (0x00) characters
        date = date.split('\0',1)[0]
        dateArray = date.split(':')
        date=dateArray[0]+"-"+dateArray[1]+"-"+dateArray[2]+":"+dateArray[3]+":"+dateArray[4]
        pattern = '%Y-%m-%d %H:%M:%S'
        epoch = datetime.datetime.strptime(date, pattern).timestamp()
    except (Exception) as error:
        logger.debug("exif data error")
        logger.debug(imagefullname)
        logger.debug(error)
        logger.debug("falling back on file creation date")
        try:
            epoch = creation_date(imagefullname)
            date = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')
        except(Exception)as error2:
            logger.error("no date informtion for file {}".format(imagefullname))
            logger.error(error2)

    return date, epoch
