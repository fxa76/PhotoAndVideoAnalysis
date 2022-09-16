import os
import platform
import logging.config
import argparse

logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

def get_files_on_disk(basedirectory):
    logger.info("Starting to scan file storage for images and videos")
    j=0
    files_on_disk ={}
    acceptable_extensions = ('mp4','mov','mpg','avi','3gp','png','tiff','jpg','jpeg','orf','raw','webm','webp')
    for root, dirs, files in os.walk(basedirectory, topdown = False):
        for name in files:
            #logger.debug("checking file : {}".format(name))
            j=j+1
            if (name.lower().endswith(tuple(acceptable_extensions))):
                filefullname = os.path.join(root, name)
                files_on_disk[filefullname]=[filefullname,root,name]

    logger.info("number of files in {} : {}".format(basedirectory,len(files_on_disk)))
    return files_on_disk



if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--target", required=True,
        help="target directory to be scanned")
    args = vars(ap.parse_args())

    get_files_on_disk(args['target'])
