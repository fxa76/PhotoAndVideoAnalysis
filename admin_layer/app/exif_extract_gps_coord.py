from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS
from PIL import Image


#local imports
import logging.config

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

def get_gps_coord(imagefullname):
    lat = None
    lon = None
    coord_from_exif = False
    try:
        exif = get_exif(imagefullname)
        geotags = get_geotagging(exif)
        lat,lon =get_coordinates(geotags)
        coord_from_exif = True
    except (Exception) as error:
        logger.error("error getting lat lon from exif : {}".format(error))

    return lat,lon,coord_from_exif


def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if key in exif[idx]:
                    geotagging[val] = exif[idx][key]

    return geotagging

def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds
    return round(degrees + minutes + seconds, 5)

def get_coordinates(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return lat,lon

if __name__ == '__main__':
    print("testing gps coord")
    lat,lon,fromExif = get_gps_coord("c:/tmp/20200401_150504.jpg")
    print("{}/{}/{}".format(lat,lon,fromExif))
