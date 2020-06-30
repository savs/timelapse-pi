import boto3
from consolemenu.prompt_utils import PromptUtils
from consolemenu import ConsoleMenu, Screen
import os
from consolemenu.items import FunctionItem
from util import run, clearDir, log
from config import getConfig

client = boto3.client('s3')
screen = Screen()
s3 = boto3.resource('s3')
bucket = s3.Bucket('atlascampi')


def listAllKeys():
    for obj in bucket.objects.all():
        print(obj.key)


def getDays():
    log('Getting days...')
    # Get list of files
    items = []
    for obj in bucket.objects.all():
        split = obj.key.split('/')
        items.append(f'{split[1]}')

    # Get distinct days
    daySet = set(items)
    days = []
    for day in daySet:
        days.append(day)
    days.sort()

    return days


def getArchiveDays():
    log('Getting days...')
    # Get list of files
    items = []
    for obj in s3.Bucket('atlascampi-archive').objects.all():
        split = obj.key.split('/')
        items.append(f'{split[1]}')

    # Get distinct days
    daySet = set(items)
    days = []
    for day in daySet:
        days.append(day)
    days.sort()

    return days


def sync(prompt=True):
    clearDir('../data/s3')
    run(["aws", "s3", "sync", "s3://atlascampi", "../data/s3", "--only-show-errors"])
    if prompt:
        PromptUtils(screen).enter_to_continue()


def syncDay(day):
    log(f'Syncing day: {day}')
    for node in getConfig()["activeCams"]:
        run(["aws", "s3", "sync",
            f"s3://atlascampi/{node}/{day}", f"../data/s3/{node}/{day}", "--only-show-errors"])


def syncArchiveDay(day):
    log(f'Syncing day: {day}')
    for node in getConfig()["activeCams"]:
        run(["aws", "s3", "sync",
            f"s3://atlascampi-archive/{node}/{day}", f"../data/s3/{node}/{day}", "--only-show-errors"])


def cleanLocal():
    os.system("rm -rf ../data/s3/*")
    PromptUtils(screen).enter_to_continue()


def getBucketSize(bucket):
    total_size = 0
    bucket = s3.Bucket(bucket)
    for object in bucket.objects.all():
        total_size += object.size
    return formatBytes(total_size)


def formatBytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0: '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'bytes'


def listBucketSizes():
    print(f"atlascampi:         {getBucketSize('atlascampi')}")
    print(f"atlascampi-archive: {getBucketSize('atlascampi-archive')}")
    print(f"atlas-timelapse:    {getBucketSize('atlas-timelapse')}")
