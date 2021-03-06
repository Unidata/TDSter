import urllib2
import os
from helpers.fileName_helper import getOutFilePath
from helpers.http_helper import basic_http_request
import xml.etree.ElementTree as ET
import json
import io
import datetime as dt

outFilePath = ""
testing = False

def scrapeServerInfo(testServer):
    global outFilePath
    # get serverInfo.txt for the selected server, and save it out for javascript page to access
    #serverInfoUrl = testServer + "thredds/serverVersion.txt"
    serverInfoUrl = testServer + "thredds/info/serverInfo.xml"
    response = basic_http_request(serverInfoUrl, return_response = True)
    serverInfo = response.read()
    # cleanup and turn into list
    #serverInfo = serverInfo.replace("\r","").split("\n")
    #while serverInfo[-1] == "":
    #    serverInfo.pop(-1)
    tree = ET.fromstring(response)
    webapp = tree.findall("webapp")[0]
    jsonDataDict = {}
    jsonDataDict["name"] = webapp.find("name").text
    jsonDataDict["version"] = webapp.find("version").text
    jsonDataDict["buildDate"] = webapp.find("versionBuildDate").text
    jsonDataDict["lastCheck"] = dt.datetime.now().isoformat()

    outFileName =  os.path.join(outFilePath, "serverInfo.json")
    with io.open(outFileName, 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(jsonDataDict, ensure_ascii=False)))

def main(testServer):
    global outFilePath
    global testing

    outFilePath = getOutFilePath(testServer, testing)

    print("Getting server info for {}".format(testServer))

    scrapeServerInfo(testServer)

if __name__ == "__main__":
    from helpers.tdster_defaults import testServers
    for testServer in testServers:
        main(testServer)
