#!/usr/bin/env python3


import os
import subprocess
import argparse
import sys
import json
import unicodedata
import time
from pathlib import Path
import csv


from lib.version import version
from lib.processing import processing


baseDir = os.path.dirname(os.path.realpath(__file__))

# parse command line options
# Instantiate the parser
parser = argparse.ArgumentParser(
    description='Upload your video file to youtube')
parser.add_argument('-c', '--config', required=False,
                    help='Path to config file')
parser.add_argument('-d', '--csv', required=True,
                    help='Path to csv data file')
parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s '+version)

args = parser.parse_args()
configFile = args.config

if args.config is None:
    configFile = baseDir+"/data/config.json"     # Config
else:
    configFile = str(args.threads)

if args.csv is None:
    print("Error: Please define script argument --csv file.csv")
    sys.exit(1)
else:
    csvDataFile = args.csv

try:
    with open(configFile) as json_file:
        config = json.load(json_file)
except IOError:
    print(("Error: Cannot read config file: "+configFile))
    sys.exit(1)


logFile = baseDir+"/log/do_video.log"
processing = processing(config, logFile)


def main():
    filesForRemove = []
    processing.writeLog("Info: Script started")
    try:
        with open(csvDataFile, newline='') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=',', fieldnames=None, restkey='unknown')
            for line in reader:
                #print( line )
                processing.writeLog(
                    "Info: Start processing for line "+line['id'])
                # get youtube video_id
                tmpFile = processing.getTmpFileName('tmp')
                filesForRemove.append(tmpFile)
                cmd = processing.getVideoId(line['link'], tmpFile)
                processing.writeLog(
                    "Info: Prepared command:" + cmd)
                try:
                    if not processing.doExec(cmd):
                        processing.writeLog(
                            "Error: Cannot get videoId for url:" + line['link'])
                        continue
                except:
                    processing.writeLog(
                        "Error: Cannot get videoId for url:" + line['link'])
                    continue

                f = open(tmpFile, "r")
                if f:
                    videoId = f.read().rstrip()
                    f.close()
                    processing.writeLog(
                        "Info: VideoId :" + videoId)
                else:
                    processing.writeLog(
                        "Error: Cannot read videoId from file :" + tmpFile)
                    continue

                if not videoId:
                    processing.writeLog(
                        "Error: Cannot get videoId for url:" + line['link'])
                    continue

                # download youtube video
                tmpFile = processing.getTmpFileName('tmp')
                filesForRemove.append(tmpFile)

                cmd = processing.downloadFile(line['link'], tmpFile)
                processing.writeLog(
                    "Info: Prepared command:" + cmd)
                try:
                    if not processing.doExec(cmd):
                        processing.writeLog(
                            "Error: Cannot download video for url:" + line['link'])
                        continue
                except:
                    processing.writeLog(
                        "Error: Cannot download video for url:" + line['link'])
                    continue
                # check extenson for downloaded video
                for extension in ['.mkv', '.mp4', '.webm', '.ogg', '.flv']:
                    file = tmpFile+extension
                    if os.path.isfile(file):
                        processing.writeLog(
                            "Info: url:" + line['link'] + " downloaded to file: "+file)
                        break

                if not os.path.isfile(file):
                    processing.writeLog(
                        "Error: Cannot download file for url:" + line['link'])
                    continue

                filesForRemove.append(file)
                # prepare ffmpeg command
                outputFile = config['general']['outputDir'] + \
                    '/' + videoId + '.mp4'
                cmd = processing.ffmpegPrepareCommand(file, line, outputFile)

                processing.writeLog(
                    "Info: Prepared command:" + cmd)
                try:
                    if not processing.doExec(cmd):
                        processing.writeLog(
                            "Error: Cannot execute ffmpeg command")
                        continue
                except:
                    processing.writeLog(
                        "Error: Cannot execute ffmpeg command")
                    continue

                processing.writeLog(
                    "Info: Video was processed : "+outputFile)

    except IOError:
        print(("Error: Cannot read csv file: "+csvDataFile))
        processing.writeLog("Info: Script finished")
        processing.removeTmpFiles(filesForRemove)
        sys.exit(1)

    processing.writeLog("Info: Script finished")
    processing.removeTmpFiles(filesForRemove)
    sys.exit(0)



def csv_dict_reader(file_obj):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(file_obj, delimiter=',')
    for line in reader:
        print(line["first_name"]),
        print(line["last_name"])


if __name__ == '__main__':
    main()
