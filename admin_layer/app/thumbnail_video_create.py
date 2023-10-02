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

def get_base_64_small(img):
    try:
        #rescale img to height 700
        max_h=100
        height, width, depth = img.shape
        img_scale = max_h/height
        new_w,new_h = width*img_scale, height*img_scale
        img_small = cv2.resize(img,(int(new_w),int(new_h)))

        mask = cv2.imread('/pictures_work/videoMask.png',0)
        height, width, depth =img_small.shape
        try:
            mask = cv2.resize(mask,(width,height))
            #logger.debug(mask.shape)
            #logger.debug(img_small.shape)

        except (Exception) as error0:
            logger.error("{}".format(error0))

        res = cv2.bitwise_and(img_small,img_small,mask = mask)
        #cv2.imwrite('/pictures_work/img.png',res)
        image_base64 = get_image_base_64(res)
        return image_base64
    except (Exception) as error:
        logger.error("Error encoding small image get_base_64_small")
        logger.error('Failed to convert image to small image base 64', exc_info=True)
    return "error when converting image"

def get_thumbnail(filepath):
    vidcap = cv2.VideoCapture(filepath)
    vidcap.open(filepath)
    success,image = vidcap.read()
    count = 0
    while count<1:
      success,image = vidcap.read()
      logger.debug('Read a new frame for file {} : {}'.format(filepath,success))
      #cv2.imwrite("/pictures_work/video/frame%d.jpg" % count, image)     # save frame as JPEG file
      img = get_base_64_small(image)
      count += 1
    vidcap.release()
    return img

if __name__ == '__main__':
    logger.debug("starting video thumbnail creation")
    import os
    imagePath = '/pictures_work/test.mp4'
    if os.path.exists(imagePath):
        logger.debug("file found")
        get_thumbnail(imagePath)
    else:
        logger.debug("file NOT found")

    logger.debug("done video thumbnail creation")