import os
import shutil
import logging.config
import datetime
import random

#local imports
import file_calculate_sha
import file_duplicates_finder

#setup logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

#move a file from one source directory to a target directory
def move_file_hierarchy(fromdir,todir,src):
    logger = logging.getLogger("main")
    head, tail = os.path.split(src)
    head = head[len(fromdir):]
    logger.debug("head {}".format(head))
    logger.debug("tail {}".format(tail))
    dst = todir+src[len(fromdir):]
    logger.debug("moving : {}".format(src))

    try:
        os.makedirs(todir+head, exist_ok=True)
    except( FileExistsError) as exc:
        print("directory already exists " , exc_info=True)

    try:
        if(os.path.exists(dst)):
            name = os.path.basename(dst)
            root = os.path.dirname(dst)
            extension_dot_position = name.rfind('.')
            extension=name[extension_dot_position:]
            name = name[:extension_dot_position]
            randint= random.randint(0, 1000)
            dst="{}/{}_{}{}".format(root,name,randint,extension)
            logger.info("FILE ALREADY EXISTS !!!!!!!!!!!!!! ")
            shutil.move(src,dst)
        else:
            shutil.move(src,dst)
    except( OSError) as exc:
        print("error moving file " , exc_info=True)
    return dst

#move files in the dictionnary not moving item 0, considered to be the origginal.
def move_duplicates(duplicates,source_dir,target_dir):
    fileHandle=open("movedFiles.csv", "a+")
    try :
        cpt=1
        for k in duplicates :
            files = duplicates[k]
            for f in files[1:]:
                move_file_hierarchy(source_dir,target_dir,f)
                fileHandle.write("{},{}\r\n".format(files[0],f))
            if(cpt%100==0):
                logger.info("Moved {} group of files".format(cpt))
            cpt=cpt+1
    except( OSError) as exc :
        print("error moving file ", exc_info=True)
    finally:
        fileHandle.close()

def clean_directory(source_dir,recycle_dir):
    start = datetime.datetime.now()
    files,duplicates = file_duplicates_finder.find_duplicates_in_hierarchy(source_dir)

    logger.info("Number of duplicates found in directory : {}".format(len(duplicates)))
    logger.info("start moving {} group of files".format(len(duplicates)))
    move_duplicates(duplicates,source_dir,recycle_dir)
    logger.info("Done with analysis of directory {}".format(source_dir))

    end = datetime.datetime.now()
    time_taken = end - start
    logger.info("Time taken : {}s OR {}ms".format(time_taken.seconds,time_taken.microseconds))
