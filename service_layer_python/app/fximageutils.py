import cv2
import base64

def get_image_base_64(img):
    image_base64 = "data:image/jpg;base64,"
    try:
    	retval, buffer = cv2.imencode('.jpg', img)
    	image_base64 += base64.b64encode(buffer).decode('utf-8').replace('\n', '')
    except(Exception) as error:
        print(error)

    return image_base64

def get_roi_base_64(filefullname,x1,y1,x2,y2):

	return ""
