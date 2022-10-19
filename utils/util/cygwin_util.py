# coding: utf-8

import cv2
import subprocess
import sys
import shlex

def getgrayimage(image):
    if image.ndim == 2:
        grayscale = image
    else:
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return grayscale

def checkcygwin():
    try:
        p = subprocess.Popen(
            ['uname'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
            )
        stdout, stderr = p.communicate()
    except:
        return False
    
    if b'CYGWIN' in stdout: # running in Cygwin
        return True
    else:
        return False
    

def cygwinconversionneeded():
    
    try:
        p = subprocess.Popen(
            ['uname'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False
            )
        stdout, stderr = p.communicate()
    except:
        # not posix
        return False
    
    if b'CYGWIN' in stdout: # running in Cygwin
        if sys.platform == 'cygwin': # Cygwin Python
            return False
        else: #'win32' -> Windows Python
            return True
    else:
        return False


def cygpathconv(path):
    cmd = 'cygpath "{}"'.format(path)
    p = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False
        )
    stdout, stderr = p.communicate()
    
    return stdout.decode('utf-8').strip()
    
def escapepath(path):
    return path.replace("\\", "/")