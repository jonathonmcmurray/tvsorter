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
    Given a dict of thumbnail matches for a video, return overall closest match(es)
    """
    return [k for k,v in mins.items() if v == min(mins.values())]

def matchvideo(video,pattern):
    """
    Match a single video to a glob of thumbnails, return early if exact match is found
    """
    log(f"Beginning scan for {video}")
    # generate set of hashes to compare to
    imgs = []
    hashes = []
    for f in sorted(glob.glob(pattern)):
        imgs.append(f)
        hashes.append(imagehash.average_hash(Image.open(f)))
    
    # iterate through frames of videos until finding a match
    v = cv2.VideoCapture(video)
    s,i = v.read()
    mins = {}
    while s:
        hash = hashframe(i)
        cmp = [h - hash for h in hashes]
        mins = util.mineach(mins,dict(zip(imgs,cmp)))
        if 0 == min(cmp):
            log(f"Found an exact match with {imgs[cmp.index(0)]}")
            break
        s,i = v.read()
    
    log("Finished scanning video")
    return mins

def getmatches(final,matches):
    # iterate over all the unmatched videos remaining
    for k in list(matches):
        # k is video name
        # get closest thumbnail for this video, excluding any already there
        m = list(filter(lambda x:not x in final.values(),matches[k]))
        ms = dict([(k,v) for k,v in matches[k].items() if k in m])
        c = getclosest(ms)
        # if one single closest, take it & remove from the potentials
        if 1 == len(c):
            final[k] = c[0]
            matches.pop(k)
    # while still some potentials, recurse
    if 0<len(matches):
        final = getmatches(final,matches)
    return final
    

def allvideos(videopattern,thumbpattern):
    """
    Iterate through a glob of videos & match each one to closest thumbnail
    """
    renames = {}
    matches = {}
    # potential = {}
    for f in sorted(glob.glob(videopattern)):
        matches[f] = matchvideo(f,thumbpattern)
    #     c = getclosest(matches[f])
    #     if 1 == len(c):
    #         #renames[f] = os.path.splitext(os.path.basename(c[0]))[0] + ".mkv"
    #         renames[f] = c[0]
    #     else:
    #         potential[f] = c

    # # remove any items that have already matched perfectly
    # for f,p in potential.items():
    #     potential[f] = [x for x in p if not x in renames.values()]

    renames = getmatches({},matches)
    print('"Good" matches:')
    util.prettydict(renames)
    # print('\n"Potential matches')
    # util.prettydict(potential)
    
    # TODO add logic here to break any ties & create rename dict

    return [renames,matches]
    #return matches
