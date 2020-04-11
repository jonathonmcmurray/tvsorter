from PIL import Image
import os
import imagehash
import cv2
import glob
from datetime import datetime
import util

def log(s):
    """
    Simple basic logging output with timestamp
    """
    now = datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S") + " " + s)
    return

def hashframe(i):
    """
    Get imagehash for a frame passed as a numpy array
    """
    return imagehash.average_hash(Image.fromarray(i))

def getclosest(mins):
    """
    Given a list of closest matches for each frame, return overall closest match
    """
    cmps = [x[0] for x in mins]
    return mins[cmps.index(min(cmps))]

def matchvideo(video,pattern):
    """
    Match a single video to a glob of thumbnails, return early if exact match is found
    """
    log(f"Beginning scan for {video}")
    # generate set of hashes to compare to
    imgs = []
    hashes = []
    for f in glob.glob(pattern):
        imgs.append(f)
        hashes.append(imagehash.average_hash(Image.open(f)))
    
    # iterate through frames of videos until finding a match
    v = cv2.VideoCapture(video)
    s,i = v.read()
    mins = {}
    #found = False
    while s:
        hash = hashframe(i)
        cmp = [h - hash for h in hashes]
        mins = util.mineach(mins,dict(zip(imgs,cmp)))
        if 0 == min(cmp):
            log(f"Found an exact match with {imgs[cmp.index(0)]}")
            #found = True
            break
        s,i = v.read()
    
    #if found == False:
    #    closest = getclosest(mins)
    #    log(f"Closest match ({closest[0]}) with {closest[1]}")

    log("Finished scanning video")
    return mins

def allvideos(videopattern,thumbpattern):
    """
    Iterate through a glob of videos & match each one to closest thumbnail
    """
    renames = {}
    matches = {}
    for f in glob.glob(videopattern):
        matches[f] = matchvideo(f,thumbpattern)
        #c = getclosest(r)
        #renames[f] = os.path.splitext(os.path.basename(c[1]))[0] + ".mkv"
    
    # TODO add logic here to break any ties & create rename dict

    #return renames
    return matches
