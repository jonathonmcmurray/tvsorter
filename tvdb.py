import requests
import json
import os

# credentials for TVDB API
apikey = ""
userkey = ""
username = ""

# put credentials in a dictionary for ease of use
apiauth = {"apikey": apikey, "userkey": userkey, "username": username}

# global string to hold JWT once authenticated
jwt = ""

def authenticate(credentials):
    """
    Authenticate with TVDB API & set global JWT for use in other requests
    """
    global jwt
    r = requests.post("https://api.thetvdb.com/login",json=credentials)
    jwt = r.json()["token"]
    return

def tvdbget(path,params={}):
    """
    Send a simple HTTP GET request to TVDB using global JWT
    """
    header = {"Accept":"application/json","Authorization":"Bearer "+jwt}
    r = requests.get("https://api.thetvdb.com"+path,headers=header,params=params)
    return r.json()

def pagedget(path):
    """
    Perform a paged request on TVDB API i.e. retrieve full data set via multiple requests if required
    """
    r = tvdbget(path)
    data = r['data']
    while r['links']['next'] != None:
        r = tvdbget(path,params={'page':r['links']['next']})
        data += r['data']
    return data

def getthumb(episode,target="."):
    """
    Passed an episode dictionary, retrieves the episode thumbnail & saves with appropriate filename
    """
    fn = f"s{episode['airedSeason']:02}e{episode['airedEpisodeNumber']:02}.{episode['episodeName']}.jpg"
    fn = os.path.join(target,fn.replace(" ",""))
    url = "https://artworks.thetvdb.com/banners/"+episode['filename']
    print(f"Saving '{url}' as '{fn}'")
    with open(fn,'wb') as f:
        i = requests.get(url)
        f.write(i.content)
    return

def getallthumbs(episodes,target="."):
    """
    Passed a list of episode dictionaries, iterate to download all thumbnails
    """
    for episode in episodes:
        getthumb(episode,target)
    return
