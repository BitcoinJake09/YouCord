#YouCord - a discord bot to post new Youtube videos posted on multiple channels, created for #CryptoFam Discord - BitcoinJake09 1/31/2022
class CryptoFam:
    def __init__(self, name, vid):
        self.name = name
        self.vid = vid
    def setVid(self, v):
        self.vid = v


import json
import time
from discord import Webhook, RequestsWebhookAdapter
from requests_html import HTMLSession
from dhook import whook

session = HTMLSession()
webhook = Webhook.from_url(whook, adapter=RequestsWebhookAdapter())
webhook.send("YouCord has started - delevoped by @BitcoinJake09")

cfList = []
newVid = ""
lastVid = ""
cfs = []
sleepAmt = 5


with open('json_data.json') as json_file:
    dataJSON = json.load(json_file)
    for key, value in dataJSON.items():
            cfs.append(CryptoFam(str(key), str(value)))
            cfList.append(str(key))

webhook.send("Current Creator List: " + str(cfList))

            #print ("KEY: " + str(key) + " VALUE: " + str(value))
    #print(dataJSON)

#for cf in cfs:
    #print( cf.name, cf.vid, sep =' ' )


def getLastVideo(channelName):
    global lastVid, session
    session = HTMLSession()
    url = "https://www.youtube.com/c/"+ channelName +"/videos"
    print("checking channel: " + str(channelName))
    response = session.get(url)
    response.html.render(sleep=1, keep_page = True, scrolldown = 2, timeout=40)
    for links in response.html.find('a#video-title'):
        link = next(iter(links.absolute_links))
        return link
        break;

while(True):
    count = 0
    for cf in cfs:
        print(str(cf.name) + "'s current video: " + str(cf.vid))
        lastVideo = getLastVideo(cf.name)
        session.close()
        #print("test1: " + str(currentVideo))
        if (str(lastVideo) != str(cf.vid)):
            cfs[count].setVid(str(lastVideo))
            newVid = lastVideo
            newJson={}
            for cs in cfs:
                newJson[str(cs.name)] = str(cs.vid)
                json_dump = json.dumps(newJson)
                #print("json test: " + str(json_dump))

            with open('json_data.json', 'w') as outfile:
                outfile.write(str(json_dump))
            print("NEW VIDEO! " + str(newVid))
            webhook.send(str(cf.name) + " Just posted a New Video! " + str(newVid))
        else:
            print("no new videos found for: " + str(cf.name) + " :'(")
        count = count + 1
    time.sleep(sleepAmt)
