import pickle
import json
import pprint
import math
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from urllib import parse
from jsonmerge import merge

total = 0

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def get_bytes(size, suffix):
    size = int(float(size))
    suffix = suffix.lower()

    if suffix == 'kb' or suffix == 'kib':
        return size << 10
    elif suffix == 'mb' or suffix == 'mib':
        return size << 20
    elif suffix == 'gb' or suffix == 'gib':
        return size << 30

    return False

def size():
    total = 0   
    with open("data.json", "r") as outfile:
        outfiledata = json.load(outfile)
    for v in outfiledata:
        # print(v)
        for f in outfiledata[v]['files']:
            # print(f)
            size = outfiledata[v]['files'][f]['size']
            raw = size.split(" ")
            try:
                by = get_bytes(raw[0], raw[1])
            except:
                print("")
            total = by + total
    retrun convert_size(total)

if __name__ == '__main__':
    main()