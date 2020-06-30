import boto3
import sched
import time
import os
from datetime import datetime
import socket

BUCKET = "atlascampi"
INTERVAL = 5
NODE = socket.gethostname()
DEV = False
TEMP_DIR = '/home/pi/dev/timelapse-pi/client/scripts/temp'


def upload(filepath, key):
    # print(f'Uploading to {key}')
    if DEV: return
    s3 = boto3.resource('s3')
    data = open(filepath, 'rb')
    s3.Bucket(BUCKET).put_object(Key=key, Body=data)
    os.system(f'rm {filepath}')


def takePic(filename):
    filepath = f'{TEMP_DIR}{filename}'
    if DEV == False: 
        os.system(f'raspistill -n -o {filepath}')
    else:
        time.sleep(2)

    return filepath

def run():
    # Main workflow
    now = datetime.now()
    filename = now.strftime('%Y-%m-%d_%H-%M-%S.jpg')
    day = now.strftime('%Y-%m-%d')

    print(f'Taking pic: {filename}')
    filepath = takePic(filename)
    upload(filepath, f'{NODE}/{day}/{filename}')


# Wipe slate clean
os.system(f'rm {TEMP_DIR}/*.jpg')
run()

# # Main loop
# s = sched.scheduler(time.time, time.sleep)


# def do_something():
#     start = datetime.now()
#     run()
#     end = datetime.now()

#     # Offset time to take pic so the interval remains consistent
#     duration = end - start    
#     interval = 0
#     if duration.total_seconds() < INTERVAL: interval = INTERVAL - duration.total_seconds()
#     s.enter(interval, 1, do_something)


# s.enter(0, 1, do_something)
# s.run()
