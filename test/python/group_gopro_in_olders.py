import os
import logging.config
import argparse
from pathlib import Path
import shutil

logging.config.fileConfig('./logging.conf')
logger = logging.getLogger(__name__)

def get_files_on_disk(basedirectory):
    logger.info("Starting to scan file storage for images and videos")
    j=0
    files_on_disk ={}
    acceptable_extensions = ('mp4','lrv','thm') #,'mov','mpg','avi','3gp','png','tiff','jpg','jpeg','orf','raw','webm','webp'
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
    ap.add_argument("-s", "--source", required=True, help="source directory to be scanned")
    ap.add_argument("-t", "--target", required=True, help="target directory for files")
    args = vars(ap.parse_args())

    filelist= get_files_on_disk(args['source'])
    d = {}
    #
    for f in filelist:
        filename, fileextension = os.path.splitext(f)
        logger.info("file {}, filename {}, filename.right(4) {}, fileextension {}".format(f,filename,filename[-4:],fileextension))
        last4digits = filename[-4:]
            
        if last4digits in d:
            d[last4digits].append(f)
        else:
            d[last4digits] = [f]
    
    logger.info("dictionnary length  {}".format(len(d)))
    for item in d:
        targetpath=args['target']+'/'+item
        Path(targetpath).mkdir(parents=True,exist_ok=True)
        filename = Path(item).suffixes
        
        for file in d[item]:
            dst = targetpath +'/' + Path(file).stem + Path(file).suffix
            logger.info("copying file {} to {}".format(file,dst))
            shutil.move(file,dst)
            