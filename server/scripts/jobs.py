from util import mkdir, run
from s3 import syncArchiveDay, getDays
from dailyProcess import processDay, notify
import os
import boto3
import glob

# downloadAllTimelapses()
def downloadAllTimelapses():
  outdir = "../data/jobs/01_thumbnails"
  mkdir(os.path.join(outdir, "timelapse01"))
  mkdir(os.path.join(outdir, "timelapse02"))
  mkdir(os.path.join(outdir, "timelapse03"))
  mkdir(os.path.join(outdir, "timelapse04"))

  bucket = boto3.resource('s3').Bucket('atlas-timelapse')
  for obj in bucket.objects.all():
    if("_original.mp4" in obj.key): continue
    if(".gif" in obj.key): continue
    print(obj.key)
    boto3.client('s3').download_file('atlas-timelapse', obj.key, os.path.join(outdir, obj.key))


def generateThumbnails():
  print("Generating thumbnails...")
  for filename in glob.iglob('../data/jobs/01_thumbnails/**/*.mp4', recursive=True):
      print(f'##############################{filename}')
      os.system(f'ffmpeg -i {filename} -vf scale=128:-1 {filename}.lolz.mp4')
# generateThumbnails()

def copyAndRenameGeneratedThumbnails():
  files = []
  for filename in glob.iglob('../data/jobs/01_thumbnails/**/*.mp4', recursive=True):
    if("00-00-00" in filename): continue
    if(".lolz." not in filename): continue
    # if("_thumbnail." in filename): 
    # ../data/jobs/01_thumbnails/timelapse04/2020-02-29.mp4.lolz.mp4
    # ../data/jobs/01_thumbnails/timelapse04/2020-02-29_thumbnail.mp4
    new = filename.replace(".mp4.lolz", "_thumbnail").replace("01_thumbnails", "02_thumbnails")
    # files.append(new)
    os.system(f'mv {filename} {new}')
  # files.sort()
  # print("\n".join(files))
# copyAndRenameGeneratedThumbnails()



# Manual sync by day
#
# From atlascampi
# aws s3 sync s3://atlascampi/timelapse0X/2020-05-22 ../data/s3 --only-show-errors
#
# From archive
# aws s3 sync s3://atlascampi-archive/timelapse0X/2020-05-23 ../data/s3/timelapse0X/2020-05-23 --only-show-errors

# Has not been tested
def processFromArchive(day):
  syncArchiveDay(day)
  processDay(day=day, skipClean=True, skipSync=True)

# Manually notify
# notify("2020-06-12")  

# print(getDays())
