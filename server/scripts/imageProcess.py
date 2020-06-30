from consolemenu import ConsoleMenu, Screen
from consolemenu.items import FunctionItem
from consolemenu.prompt_utils import PromptUtils
import os
import glob
import datetime
import astro
import s3
from util import getToday, mkdir, run, log, clearDir
from config import getConfig

screen = Screen()
DIR_S3 = "../data/s3"
DIR_S3_NODES = "../data/s3/**"
DIR_PROCESSED = "../data/processed"
DIR_PROCESSED_NODES = "../data/processed/**"
DIR_GIF_OUTPUT = "../data/gifs"
GIF_DELAY = 3
framerate = "30"


def deleteDarkImages(node, date):
    log('Deleting dark images')
    sunrise, sunset = astro.getTimes(date)

    files = glob.glob(f'../data/processed/{node}/temp/*')
    for file in files:
        fileName = os.path.basename(os.path.normpath(file))
        dotSplit = fileName.split('.')
        underscoreSplit = dotSplit[0].split('_')
        time = underscoreSplit[1].replace('-', '')

        if int(time) < int(sunrise) or int(time) > int(sunset):
            run(['rm', file], False)


# ffmpeg -t 10 -i in.mp4 -vf "fps=30,scale=100:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 out.gif
def convertImagesToMp4(framerate, dimensions, inPath, outPath):
    cmd = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel", "error",
        "-f", "image2",
        "-pattern_type", "glob",
        "-framerate", framerate,
        "-i", inPath,
        "-s", dimensions,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        outPath
    ]
    run(cmd)


# ffmpeg -i input.avi -vf scale=320:-1 output.avi
def resizeMp4(width, height, source, destination):
    cmd = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-loglevel", "error",
        "-i", source,
        "-vf", f"scale={width}:{height}",
        destination
    ]
    run(cmd)


def createPreviewGif(inPath, outPath):
    cmd = [
        "ffmpeg",
        "-y",
        "-t", "20",
        "-i", inPath,
        "-vf", "fps=30,scale=100:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
        "-loop", "0",
        outPath
    ]
    run(cmd)


def createArchiveVideo(dayPath, outputDir, day):
    log('Converting original images to mp4 (for archive)')
    convertImagesToMp4(
        framerate,
        "3280x2464",
        f"{os.path.join(dayPath, '*.jpg')}",
        os.path.join(outputDir, f'{day}_original.mp4'))

def createVideo(outputDir, dayPath, nodeName, day):
    log('Creating main video...')
    log('Copying files to temp dir')
    tempDir = os.path.join(outputDir, "temp")
    mkdir(tempDir)
    os.system(f'cp -a {dayPath}/. {tempDir}')

    deleteDarkImages(nodeName, day)

    log('Creating final video...')
    outPath = os.path.join(outputDir, f'{day}.mp4')
    convertImagesToMp4(
        framerate,
        "1024x768",
        os.path.join(tempDir, '*.jpg'),
        outPath)

    # log('Creating thumbnail video...')
    thumbPath = os.path.join(outputDir, f'{day}_thumbnail.mp4')
    resizeMp4("128", "96", outPath, thumbPath)

    log('Removing temp dir')
    os.system(f'rm -rf {tempDir}')

    return outPath


def processDay(nodeName, day):
    log(f'Processing day/node: {day}/{nodeName}')
    dayPath = f"../data/s3/{nodeName}/{day}"
    outputDir = os.path.join(DIR_PROCESSED, nodeName)
    mkdir(outputDir)

    createArchiveVideo(dayPath, outputDir, day)
    videoPath = createVideo(outputDir, dayPath, nodeName, day)
    createPreviewGif(videoPath, os.path.join(outputDir, f'{day}.gif'))


def processImagesByDay(day):
    log(f"Imagine processing: {day}")
    for node in getConfig()["activeCams"]:
        processDay(node, day)
