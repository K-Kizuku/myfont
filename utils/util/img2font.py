# -*- coding: utf-8 -*-
from tkinter import E
import cv2
import os
import glob
import re

import json
import subprocess


# potrace command
POTRACE = 'potrace'
CHARS_COUNT = 0    


def passpotrace(image, optionargs=[]): 

    retval, buf = cv2.imencode('.bmp', image)
    if retval == False:
        raise ValueError('The Given image could not be converted to BMP binary data')
    
    binbmp = buf.tobytes()
    
    args = [
        POTRACE,
        '-', '-o-', '--svg'
    ] + optionargs
    
    p = subprocess.Popen(
        args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False
        )
    
    stdout, stderr = p.communicate(input=binbmp)
    if len(stderr) == 0:
        binsvg = stdout
    else:
        raise RuntimeError('Potrace threw error:\n' + stderr.decode('utf-8'))
        
    return binsvg

def saveasfile(outdir, name, bsvg):
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    outpath = os.path.join(outdir, name+".svg")
    with open(outpath, "wb") as w:
        w.write(bsvg)

def scanchars(img, outdir, exist_chars_lsit):
    global CHARS_COUNT

    size_w, size_h = 256, 256

    _x = 0
    while(_x < len(img[0,:,0])):
        _y = 0
        while(_y < len(img[:,0,0])):
            name = hex(ord(exist_chars_lsit[CHARS_COUNT]))[2:]
            name = name.zfill(4)
            _img = img[_y:_y+size_h , _x:_x+size_w]
 
            grayimg = cv2.cvtColor(_img, cv2.COLOR_BGR2GRAY)
            grayimg = cv2.resize(grayimg, (1000,1000))
            _, binimg = cv2.threshold(grayimg,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

            optargs = []
            bsvg = passpotrace(binimg, optargs)
            bsvg = bsvg.replace(b"pt", b"px")


            if outdir != '' and not os.path.isdir(outdir):
                os.makedirs(outdir)
            saveasfile(outdir, name, bsvg)

            _y += size_h

            CHARS_COUNT += 1
            if CHARS_COUNT == len(exist_chars_lsit) :
                break

        _x += size_w



def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def addfiles(lstfile, dstdir, exist_chars_list_path, verbose=True ):
    exist_chars_list = json.load(open(exist_chars_list_path))["jp"]

    def _processonefile(path):
        if os.path.isdir(path): # if folder
            path_list = sorted(glob.glob(os.path.join(path, "*.png")), key=natural_keys)
            addfiles(path_list, dstdir,exist_chars_list_path ,verbose)
        elif os.path.isfile(path):
            #convert image
            if verbose:
                print("Processing {}:".format(path))
            img = cv2.imread(path)
            scanchars(img, dstdir, exist_chars_list)
        else:
            print("{}: File not found!".format(path))

    if isinstance(lstfile, list):
        for path in lstfile:
            _processonefile(path)
    elif isinstance(lstfile, str):
        _processonefile(lstfile)

