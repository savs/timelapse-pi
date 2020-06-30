import boto3
import datetime
import shutil
import os


def minDate(items):
    list = [
        items["timelapse01"][0],
        items["timelapse02"][0],
        items["timelapse03"][0],
        items["timelapse04"][0]
    ]
    list.sort()
    return list[0]


def dateToString(date): return date.strftime("%Y-%m-%d")


def contains(date, list): return date in list


def videoDateToString(videoData):
    return (
        f"timelapse01: {videoData['timelapse01']}\n"
        f"timelapse02: {videoData['timelapse02']}\n"
        f"timelapse03: {videoData['timelapse03']}\n"
        f"timelapse04: {videoData['timelapse04']}\n"
    )


def getFileContent(date, videoData):
    return (
        "---\n"
        "layout: post\n"
        f"title: \"{date}\"\n"
        f"date: {date} 00:00:00 +0000\n"
        f"{videoDateToString(videoData)}"
        "---\n"
    )


client = boto3.client('s3')
s3 = boto3.resource('s3')
bucket = s3.Bucket('atlas-timelapse')

items = {
    "timelapse01": [],
    "timelapse02": [],
    "timelapse03": [],
    "timelapse04": []
}

print("Get files from S3")
for obj in bucket.objects.all():
    key = obj.key

    if(key.find("_original") >= 0):
        continue
    if(key.find(".gif") >= 0):
        continue
    if(key.find("00-00-00") >= 0):
        continue
    if(key.find(".DS_Store") >= 0):
        continue

    camNumber = key.split("/")[0]
    fileName = key.split("/")[1]
    items[camNumber].append(fileName.replace(".mp4", ""))

print("Sort")
items["timelapse01"].sort()
items["timelapse02"].sort()
items["timelapse03"].sort()
items["timelapse04"].sort()

print("Clear existing posts")
shutil.rmtree("../flexible-jekyll/_posts", ignore_errors=True)
os.mkdir("../flexible-jekyll/_posts")

print("Enumerate days")
startDate = datetime.datetime(2020, 1, 3)
endDate = datetime.datetime.now()
days = {}
currentDate = startDate
while True:
    days[dateToString(currentDate)] = {
        "timelapse01": contains(dateToString(currentDate), items["timelapse01"]),
        "timelapse02": contains(dateToString(currentDate), items["timelapse02"]),
        "timelapse03": contains(dateToString(currentDate), items["timelapse03"]),
        "timelapse04": contains(dateToString(currentDate), items["timelapse04"])
    }
    with open(f"../flexible-jekyll/_posts/{dateToString(currentDate)}-{dateToString(currentDate)}.markdown", "w") as f:
        f.write(getFileContent(dateToString(currentDate),
                               days[dateToString(currentDate)]))

    currentDate = currentDate + datetime.timedelta(days=1)
    if(dateToString(currentDate) == dateToString(endDate)):
        break

print("Build site")
os.system("cd ../flexible-jekyll && bundle exec jekyll build")

print("Copy to web repo")
os.system("cp -R ../flexible-jekyll/_site/ ../../../portlapse.com/")
os.system("rm ../../../portlapse.com/Gemfile")
os.system("rm ../../../portlapse.com/Gemfile.lock")

print("Save")
os.system("cd ../../../portlapse.com && git add .")
os.system("cd ../../../portlapse.com && git commit -amboop")
os.system("cd ../../../portlapse.com && git push")
