import datetime
import os
import subprocess
import shutil

def clearDir(dir):
    log(f'Clearing dir: {dir}')
    run(["rm", "-rf", dir], False)
    mkdir(dir, False)


def getToday():
    today = datetime.datetime.today()
    return today.strftime('%Y-%m-%d')

def log(msg, printMsg=True, file=None):
    time = datetime.datetime.today().strftime('[%Y-%m-%d %H:%M:%S]')
    if printMsg:
        print(f'{time} {msg}')
    if file:
        file.write(f'{time} {msg}\n')
    else:
        with open('../logs/output.txt', 'a') as file:
            file.write(f'{time} {msg}\n')


def run(cmd, logMsg=True):
    errMsg = 'Error running command. See logs, exiting...'
    with open('../logs/output.txt', 'a') as out:
        if logMsg:
            log(f'Running: {" ".join(cmd)}', file=out)
    with open('../logs/output.txt', 'a') as out:
        return_code = subprocess.call(cmd, stdout=out, stderr=out)
        if return_code != 0:
            log(errMsg, out)

    if return_code != 0:
        raise SystemExit(errMsg)

    return return_code


def mkdir(path, logMsg=True):
    """Create dir, ignore if it exists"""
    try:
        if(logMsg): 
            log(f'Creating dir: {path}')
        os.mkdir(path)
    except OSError as ex:
        if ex.errno != 17:
            raise ex

def moveFiles(sourceDir, destDir):
    cmd = f"mv {sourceDir} {destDir}"
    log(cmd)
    os.system(cmd)

