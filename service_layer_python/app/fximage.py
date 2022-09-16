from __future__ import print_function # In python 2.7
import sys
import cv2
import base64
import fximageutils
import seaborn as sns
import datetime


class FXImage(object):
    def __init__(self,image_id, filefullname, filename, filepath, fileextensions, filesize, creationdate,comments):
        self.image_id = image_id
        self.filefullname = filefullname
        self.filename = filename
        self.filepath = filepath
        self.fileextensions = fileextensions
        self.filesize = filesize
        self.creationdate = creationdate
        self.comments = comments
        self.objs = []
        self.to_be_deleted = None
        self.thumbnail = None
        self.image_base64 = None
        self.image_base64_overlay = None
        self.othernames=[]
        self.lat = None
        self.lon = None
        self.timestamp = ""
        self.width = 0
        self.height = 0
        self.depth = 0

    def get_date_str(self):
        date = "undefined"
        if self.creationdate is not None:
            date = datetime.datetime.fromtimestamp(self.creationdate).strftime('%Y-%m-%d %H:%M:%S')
        return date;

    def get_base_64_small(self):
        try:
            #print("rescalling")
            img = cv2.imread(self.filefullname, 1)
            #rescale img to height 700
            maxH=100
            height, width, depth = img.shape
            imgScale = maxH/height
            newW,newH = width*imgScale, height*imgScale
            img_small = cv2.resize(img,(int(newW),int(newH)))
            image_base64 = fximageutils.get_image_base_64(img_small)
            self.image_base64 = image_base64
        except (Exception) as error:
            print(error, file=sys.stderr)
        return "error when converting image"

    def get_base_64(self):
        print("reading image from file : {}".format(self.filefullname) )
        image_base64 = None
        try:
            img = cv2.imread(self.filefullname, 1)
            print("fxa test")
            self.height, self.width, self.depth = img.shape
            image_base64 = fximageutils.get_image_base_64(img)
        except (Exception) as error:
            print(error)
        self.image_base64 = image_base64

    def get_base_64_overlayed(self):
        palette = sns.color_palette("Paired", 1000)
        palette2 = []
        for color in palette:
        	color2 =[]
        	for value in color:
        		value *= 255
        		color2.append(value)
        	palette2.append(color2)

        #print("reading image from file : {}".format(self.filefullname), file=sys.stderr )
        try:
            img = cv2.imread(self.filefullname, 1)
            self.height, self.width, self.depth = img.shape
        except Exception as error:
            self.height, self.width, self.depth = 10,10,10
            print(error, file = sys.stderr)
        #print("image content is : {}".format(img),file=sys.stderr)
        #display objects ROI on the image
        i=0
        for img_obj in self.objs:
            x=20
            y=30
            if img_obj.description == 'nothing_found' or img_obj=='error_on_detection' or img_obj.description == 'no_face_found' :
                pass
            else:
                try:
                    print("data description : {}".format(img_obj.description ))
                    print("data for rectangle x:{},y:{},h:{},w:{}".format(img_obj.x,img_obj.y,img_obj.w,img_obj.h))
                    cv2.rectangle(img,(img_obj.x,img_obj.y),(img_obj.x+img_obj.w,img_obj.y+img_obj.h),palette2[i],3)
                except (Exception) as error:
                    print(error, file=sys.stderr)

                x= img_obj.x
                y= img_obj.y
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img,"{} ({:.2f})".format(img_obj.description,img_obj.confidence),(x,y), font, 1,palette2[i],2,cv2.LINE_AA)
            i=i+1
        #create a base 64 text version of the image
        image_base64 = fximageutils.get_image_base_64(img)
        self.image_base64_overlay =  image_base64
        #print("reading image overlay is : {}".format(self.image_base64_overlay), file=sys.stderr )
