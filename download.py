import json
import math
import os
import requests
import gdown
import glob
from pyunpack import Archive
import sys
import wget

# start = 560
start = 1
count = requests.get('https://chorus.fightthe.pw/api/count')
count = str(count.json())
count = 5800
skip = '0'
priv = '1'
file2 = ""

path = "F:\\Games\\CLONE HERO"

def make_dir(name):
    global skip
    global priv
    global path2
    split = name.split("/")
    for i in split:
        if priv != '1':
            path2 = priv+"/"+i
        else:
            path2 = path+"/songs/"+i
            priv = '1'
        isFile = os.path.exists(path2)
        if isFile == False:
            os.mkdir(path2)
            os.chdir(path2)
            priv = path2
    else:
        print("dir already exists")
        # name = name + "(1)"
        pass
        # make_dir(name)
        # skip = "1"

def type(i):
    global skip
    global priv
    global path2
    global file2
    os.chdir(path)
    with open("C:\\Users\\alex\\Desktop\\chorus downloader\\data.json", "r") as jsonfile:
        data = json.load(jsonfile)
        name = data[i]['name']
        make_dir(name)
        # print(skip)
        if str(skip) == "0":
            current_files = os.listdir()
            files = data[i]['files']
            for file in files:
                if file == "ini":
                    file2 = "song.ini"
                elif file == "chart":
                    file2 = "notes.chart"
                if file2 in current_files:
                    print("match")
                else:
                    link = data[i]['files'][file]['link']
                    if file == "archive":
                        pass
                        # downlaod_archive(name, link, str(path+"/songs/"+name))
                    else:
                        # pass
                        downlad_folder(name, link)
        else:
            print("skiped song: " + name)
            skip = '0'

def downlaod_archive(name, link, path):
    gdown.download(link, quiet=False)
    for file in glob.glob("*.zip"):
        Archive(file).extractall('.')
        os.remove(file)
    for file in glob.glob("*.rar"):
        pass
def downlad_folder(name, link):
    # filename = wget.download(link)
    gdown.download(link, quiet=False)

def main():
    global path
    for i in range(int(start), int(count)):
        print("---------")
        print("Currently working on song number: " + str(i))
        print("---------")
        # try:
        os.chdir(path)
        type(str(i))
        # except KeyboardInterrupt:
            # exit(0)
        # except:
            # print("ERROR on song: " + str(i))

if __name__ == '__main__':
    path2 = path+"/songs"
    isFile = os.path.exists(path2)
    if isFile == False:
        os.mkdir(path+"/songs")
    main()
