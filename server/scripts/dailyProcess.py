from s3 import sync, getDays, getArchiveDays, syncDay
from imageProcess import processImagesByDay
from util import getToday, run, clearDir, moveFiles, log, mkdir
from config import getConfig
import os
import requests
import json
import glob
import datetime

def runDailyProcess():
    days = getDays()
    for day in days:
        if getToday() == day:
            continue
        processDay(day)


def processDay(day, skipClean=False, skipSync=False):
    log(f'Processing day: {day}')
    if(not skipClean): cleanSlate()
    if(not skipSync): syncDay(day)
    processImagesByDay(day)
    saveArtifacts(day)
    archive(day)
    notify(day)
    log(f'Done Processing day: {day}')


def notify(day):
    nodeLabels = {
        "timelapse01": "North",
        "timelapse02": "East",
        "timelapse03": "South",
        "timelapse04": "West"
    }
    for node in getConfig()["activeCams"]:
        notifySlack(day, nodeLabels[node],
                    f"https://atlas-timelapse.s3.amazonaws.com/{node}/{day}.mp4", f"https://atlas-timelapse.s3.amazonaws.com/{node}/{day}.gif")


def cleanSlate():
    clearDir('../data/s3')
    clearDir("../data/processed")
    clearDir('../data/timelapse')


def notifySlack(day, direction, mp4Link, gifLink):
    content = {
        "channel": "#pdx-timelapse",
        "username": "Timey McLapse Face",
        "blocks": [
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<{mp4Link}|{day}: {direction}>"
                },
                "accessory": {
                    "type": "image",
                    "image_url": f"{gifLink}",
                    "alt_text": f"{day}: {direction}"
                }
            }
        ]
    }
    requests.post(
        getConfig()["slackWebhook"],
        data=json.dumps(content))

def saveArtifacts(day):
    log("Saving artifacts")

    for node in getConfig()["activeCams"]:
        mkdir(f"../data/timelapse/{node}")

    # Only works with `os.system` *shrug*
    for node in getConfig()["activeCams"]:
        os.system(f"mv ../data/processed/{node}/* ../data/timelapse/{node}")
    
    run(['aws', 's3', 'sync', '../data/timelapse',
         's3://atlas-timelapse', '--only-show-errors'])


def archive(day):
    log("Archiving raw images")
    for node in getConfig()["activeCams"]:
        run(['aws', 's3', 'sync', f's3://atlascampi/{node}/{day}',
            f's3://atlascampi-archive/{node}/{day}', '--only-show-errors'])

    log("Clear raw images from S3 (exclude today)")
    if day != getToday():
        for node in getConfig()["activeCams"]:
            os.system(
                f'aws s3 rm s3://atlascampi/{node}/{day} --recursive --exclude "*/{getToday()}/*"')
    
    clearArchive()


# Clear archived more than a week old
def clearArchive():
    log("Clearing old archived images")
    retainLastXDays = 5
    days = getArchiveDays()
    deleteDays = days[0:len(days) - retainLastXDays]
    for day in deleteDays:
        log(f'Deleting {day}...')
        for node in getConfig()["activeCams"]:
            os.system(
                f'aws s3 rm s3://atlascampi-archive/{node}/{day} --recursive')


def getDay(offset):
    today = datetime.datetime.today()
    date = today - datetime.timedelta(days=offset)
    return date.strftime('%Y-%m-%d')

if __name__ == "__main__":
    runDailyProcess()