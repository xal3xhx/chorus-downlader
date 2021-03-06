import json
import math
import os
import requests
import gdown
import glob
from pyunpack import Archive
import sys
import wget
import io

# start = 560
start = 1
# change out to count the total entries in the data.json
# count = requests.get('https://chorus.fightthe.pw/api/count')
# count = str(count.json())
count = 5800

skip = '0'
priv = '1'
file2 = ""

path = "F:\\Games\\CLONE HERO"

with open("C:\\Users\\alex\\Desktop\\chorus downloader\\data.json", "r") as jsonfile:
        data = json.load(jsonfile)

def strip_end(text, suffix):
    if not text.endswith(suffix):
        return text
    return text[:len(text)-len(suffix)]

def make_dir(name):
    cwd = os.getcwd()
    global skip
    global priv
    global path
    global path2
    split = name.split("/")
    for i in split:
        i = strip_end(i, " ")
        cwd = os.getcwd()
        if priv != '1':
            cwd = os.getcwd()
            path2 = priv+"/"+i
        else:
            cwd = os.getcwd()
            path2 = path+"/songs/"+i
            priv = path2
        isFile = os.path.exists(path2)
        if isFile == False:
            cwd = os.getcwd()
            os.mkdir(path2)
            os.chdir(path2)
            priv = path2
        else:
            cwd = os.getcwd()
            pass
            # name = name + "(1)"
            # pass
            # make_dir(name)
            # skip = "1"

def type(i):
    global skip
    global priv
    global path
    global path2
    global file2
    global data
    os.chdir(path)
    name = data[i]['name']
    print("Currently working on song: " + name)
    make_dir(name)
    os.chdir(path2)
    # print(skip)
    if str(skip) == "0":
        cwd = os.getcwd()
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
                    # print("skiping archive")
                    log_path = path + "/archive_log.txt"
                    log = io.open(log_path, "r", encoding="utf-8")
                    if name not in log.read():
                        print("downloading archrive: " + name)
                        with io.open(log_path, "a", encoding="utf-8") as outfile:
                            outfile.write(name + "\n")
                        downlaod_archive(name, link, os.getcwd())
                    else:
                        print("archrive has already been downloaded.")

                    # print("downloading file:    " + name)
                    # downlad_folder(name, link)
                    # downlaod_archive(name, link, str(path+"/songs/"+name))
                else:
                    print("downloading file:    " + file)
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
        print("archrive is a RAR, please run extract_rar.bat")

def downlad_folder(name, link):
    # filename = wget.download(link)
    gdown.download(link, quiet=False)

def main():
    global path
    global path2
    global priv
    for i in range(int(start), int(count)):
        print("---------")
        print("Currently working on song number: " + str(i))
        # print("---------")
        try:
            os.chdir(path)
            priv = '1'
            path2 = ""
            type(str(i))
        except KeyboardInterrupt:
            exit(0)
        except:
            print("ERROR on song: " + str(i))

def main_dev():
    global path
    global path2
    global priv
    for i in range(int(start), int(count)):
        print("---------")
        print("Currently working on song number: " + str(i))
        os.chdir(path)
        priv = '1'
        path2 = ""
        type(str(i))

if __name__ == '__main__':
    # path2 = path+"/songs"
    # isFile = os.path.exists(path2)
    # if isFile == False:
        # os.mkdir(path+"/songs")
    main()
