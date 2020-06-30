import s3
import boto3
import os
import glob
import datetime

BUCKET = "atlas-timelapse"
TIMELAPSE_DIR = "../data/timelapse"
PROCESSED_NODES = "../data/processed/**"

def isToday(day):
    today = datetime.datetime.today()
    return today.strftime('%Y-%m-%d') == day

def upload():
    os.system(f"aws s3 sync {TIMELAPSE_DIR} 's3://atlas-timelapse' --exclude '*.DS_Store*'")

def mkdir(path):
    """Create dir, ignore if it exists"""
    try:
        os.mkdir(path)
    except OSError as ex:
        if ex.errno != 17:
            raise ex

def getNodes():
    nodes = []
    dirs = glob.glob(PROCESSED_NODES)
    for dir in dirs:
        dirName = os.path.basename(os.path.normpath(dir))
        nodes.append(dirName)
    return nodes

def archive():
    # print(getNodes())
    os.system(f'')

archive()


# TODO
# - Move from processed to timelapse dir
# - Sync timelapse dir, local -> remote
# - Empty timelapse dir
# - Delete s3 images locally
# - Delete s3 images remotely
#
#