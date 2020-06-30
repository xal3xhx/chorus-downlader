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
import requests


# get latest with offset, https://chorus.fightthe.pw/api/latest?from=0
# get total count, https://chorus.fightthe.pw/api/count

# pages = 1
start_song = 9139
start_song_page = math.ceil(int(start_song) / 20)

total = 0   
start = 1
count = requests.get('https://chorus.fightthe.pw/api/count')
count = str(count.json())
pages = math.ceil(int(count) / 20)

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

data = {}

def percentage(part, whole):
  return 100 * float(part)/float(whole)

def getsize(id):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    try:
        # Call the Drive v3 API
        request = service.files().get(fileId=id, fields='*')
        response = request.execute()
        # pprint.pprint(response)
        if 'size' in response:
            size = response['size']
            # print(size)
        else:
            size = 0

        return size
    except:
        return 'error'

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def write_file(data, filename):
    json_object = json.dumps(data, indent = 4) 
    with open(filename, "w") as outfile:
        outfile.write(json_object)
    cat_json("data.json", "dump.json")
    data = {}

def write_file1(data, filename):
    json_object = json.dumps(data, indent = 4) 
    with open(filename, "w") as outfile:
        outfile.write(json_object)
    data = {}

def cat_json(out, in1):
    outfile = open(out, "r")
    with open(out) as outfile:
        outfiledata = json.load(outfile)
    with open(in1) as infile1:
        infile1data = json.load(infile1)

    result = merge(outfiledata, infile1data)

    write_file1(result, "data.json")

def get_bytes(size, suffix):
    size = int(float(size))
    suffix = suffix.lower()
    if suffix == 'b':
        return size
    if suffix == 'kb' or suffix == 'kib':
        return size << 10
    elif suffix == 'mb' or suffix == 'mib':
        return size << 20
    elif suffix == 'gb' or suffix == 'gib':
        return size << 30

    return False

def size2():
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
                pass
            total = by + total
            # print(total)
    return convert_size(total)

def main():
    print("starting")
    # print(size2())
    for x in range(start_song_page, pages):
        
        print()
        print("---------------")
        print("CURRENT PAGE IS: " + str(x))
        global start
        # global start_song
        if start == 1:
            y = start_song
            start = 0
        else:
            y = x*20

        response = requests.get('https://chorus.fightthe.pw/api/latest?from=' + str(y))
        jsonResponse = response.json()


        for x in range(20):
            offset = x+y
            name = jsonResponse['songs'][x]['name']
            link = jsonResponse['songs'][x]['link']
            direct = jsonResponse['songs'][x]['directLinks']

            print("TOTAL NUMBER OF SONGS: " + str(count))
            print("CURRENT SONG OFFEST IS: " + str(offset))
            print("CURRENT SONG IS: " + name)
            print("percentage done is: " + str(round(percentage(offset, count),2)) + "%")
            print("total size so far: " + size2())
            print("---------------")


            data = {}
            data[offset] = {}
            data[offset]['name'] = name
            data[offset]['files'] = {}
            for k, v in direct.items():
                id = dict(parse.parse_qsl(parse.urlsplit(v).query))
                id = id['id']
                raw_size = getsize(str(id))
                if raw_size != 'error': 
                    size = convert_size(int(raw_size))
                else:
                    size = raw_size
                data[offset]['files'][k] = {}
                data[offset]['files'][k]['size'] = size
                data[offset]['files'][k]['link'] = v
            if size != 'error': 
                write_file(data, "dump.json")
            else:
                data = {}
        print("---------------")

if __name__ == '__main__':
    main()