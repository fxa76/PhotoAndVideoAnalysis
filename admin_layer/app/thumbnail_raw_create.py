import rawpy
import imageio
import cv2
import base64
import psycopg2
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
        logger.error("Error encoding get_image_base_64")
        logger.error('Failed to convert image to base 64', exc_info=True)

    return image_base64

def get_base_64_small(rgb):
    try:

        img = rgb
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
            logger.error("Error encoding small image get_base_64_small")
            logger.error('Failed to convert image to small image base 64', exc_info=True)
        return "error when converting image"

    except (Exception) as error:
        logger.error("Error reading file")


def get_thumbnail(path):
    try:
        with rawpy.imread(path) as raw:
            rgb = raw.postprocess()
            bgr = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
            return get_base_64_small(bgr)
    except(Exception) as error:
        print(error)
