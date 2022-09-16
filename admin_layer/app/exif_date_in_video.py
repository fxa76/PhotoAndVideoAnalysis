#!/usr/bin/python

# from https://stackoverflow.com/questions/21355316/getting-metadata-for-mov-video

import datetime
import struct
import sys
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

def get_mov_timestamps(filename):
    ''' Get the creation and modification date-time from .mov metadata.

        Returns None if a value is not available.
    '''
    from datetime import datetime as DateTime
    import struct
    creation_time = None
    epoch = None
    ATOM_HEADER_SIZE = 8
    # difference between Unix epoch and QuickTime epoch, in seconds
    EPOCH_ADJUSTER = 2082844800

    creation_time = modification_time = None
    src = None

    try:
        # search for moov item
        with open(filename, "rb") as f:
            while True:
                atom_header = f.read(ATOM_HEADER_SIZE)
                #~ print('atom header:', atom_header)  # debug purposes
                if atom_header[4:8] == b'moov':
                    break  # found
                else:
                    atom_size = struct.unpack('>I', atom_header[0:4])[0]
                    f.seek(atom_size - 8, 1)

            # found 'moov', look for 'mvhd' and timestamps
            atom_header = f.read(ATOM_HEADER_SIZE)
            if atom_header[4:8] == b'cmov':
                raise RuntimeError('moov atom is compressed')
            elif atom_header[4:8] != b'mvhd':
                raise RuntimeError('expected to find "mvhd" header.')
            else:
                src = 1
                f.seek(4, 1)
                creation_time = struct.unpack('>I', f.read(4))[0] - EPOCH_ADJUSTER
                creation_time = DateTime.fromtimestamp(creation_time)
                if creation_time.year < 1990:  # invalid or censored data
                    creation_time = None

                modification_time = struct.unpack('>I', f.read(4))[0] - EPOCH_ADJUSTER
                modification_time = DateTime.fromtimestamp(modification_time)
                if modification_time.year < 1990:  # invalid or censored data
                    modification_time = None

        logger.debug("Creation time is {}".format(creation_time))
        print("Creation time is {}".format(creation_time))


        epoch = creation_time.timestamp()
        creation_time = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')
    except(Exception) as error:
        logger.debug("falling back on file creation date")
        try:
            src= 2
            epoch = creation_date(filename)
            creation_time = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')
        except(Exception)as error2:
            logger.error("no date informtion for file {}".format(filename))
            logger.error(error2)

    return creation_time, epoch, src

if __name__ == '__main__':

    testfile= '/pictures_inbox/2019_android/20191225_085728.mp4'
    creation_time, epoch,src = get_mov_timestamps(testfile)
    print("{} / {} src {}".format(creation_time, epoch,src))
