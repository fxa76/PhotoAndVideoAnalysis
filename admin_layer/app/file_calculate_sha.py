#!/usr/bin/env python
import sys
import hashlib

def calculate_hash(filefullname):
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    sha512 = hashlib.sha512()
    print("calculating sha for {}".format(filefullname))
    with open(filefullname, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha512.update(data)

    return sha512.hexdigest()
