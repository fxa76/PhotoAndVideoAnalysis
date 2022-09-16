import os
import datetime
import logging.config

#local imports
import file_calculate_sha

#setup logging
logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)

#scan a folder tree to find if duplicates exist in it
#move duplicates into
def get_files_on_disk(basedirectory):
    j=0
    files_on_disk ={}
    acceptable_extensions = ['mov','mpg','avi','png','tiff','jpg','jpeg','orf','3gp','mov','webm','raw','mp4']
    for root, dirs, files in os.walk(basedirectory, topdown = False):
        for name in files:
            j=j+1
            if (name.lower().endswith(tuple(acceptable_extensions))):
                filefullname = os.path.join(root, name)
                filesize = os.path.getsize(filefullname)
                logger.debug("file : {} ({})".format(filefullname,filesize))
                #if(  filesize > 200000000):
                #print("file : {} ({})".format(filefullname,filesize))
                sha512 = file_calculate_sha.calculate_hash(filefullname)
                if sha512 in files_on_disk:
                    logger.debug("Similare SHA found {}".format(filefullname))
                    logger.debug("first file is {} ".format(files_on_disk[sha512][0]))
                    files_on_disk[sha512].append(filefullname)
                else:
                    files_on_disk[sha512]=[filefullname]
                if(j%100==0):
                    logger.info("Running analysis {} files".format(j))

    return files_on_disk

def get_duplicates_only(files):
    dict={}
    for key in files :
        if(len(files[key])>1):
            logger.debug("{}".format(files[key]))
            dict[key]=files[key]

    return dict

#find duplicated files in a
def find_duplicates_in_hierarchy(source_dir):
    logger.info("starting analysis of directory : {}".format(source_dir))
    files = get_files_on_disk(source_dir)
    logger.info("Number of files found in directory : {}".format(len(files)))
    duplicates = get_duplicates_only(files)
    logger.debug("duplicates are {}".format(duplicates))
    return files,duplicates

def compare_dir_hierarchy(source_dir,target_dir):
    start = datetime.datetime.now()

    logger.info("starting analysis of directory {}".format(source_dir))
    src_files= get_files_on_disk(source_dir)
    logger.info("starting analysis of directory {}".format(target_dir))
    #TODO optimize by only looking at extensions that are in the source_dir.
    target_files= get_files_on_disk(target_dir)

    files_to_add=[]
    files_to_bounce=[]
    for k in src_files:
        if k in target_files:
            files = src_files[k]
            files2= target_files[k]
            logger.info("file {} already in target directory as {} ".format(files[0],files2[0]))
            for f in src_files[k]:
                files_to_bounce.append(f)
        else:
            for f in src_files[k]:
                files_to_add.append(f)

    logger.info("Number of files to add : {}".format(len(files_to_add)))
    logger.info("Number of files to bounce : {}".format(len(files_to_bounce)))

    end = datetime.datetime.now()
    time_taken = end - start
    logger.info("Time taken : {}s OR {}ms".format(time_taken.seconds,time_taken.microseconds))

    return files_to_add,files_to_bounce
