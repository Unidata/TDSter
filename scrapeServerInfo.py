import urllib2
import os
from helpers.fileName_helper import getOutFilePath
from helpers.http_helper import basic_http_request
import json
import io

outFilePath = ""
testing = False

def scrapeServerInfo(testServer):
    global outFilePath
    # get serverInfo.txt for the selected server, and save it out for javascript page to access
    serverInfoUrl = testServer + "thredds/serverVersion.txt"
    response = basic_http_request(serverInfoUrl, return_response = True)
    serverInfo = response.read()
    # cleanup and turn into list
    serverInfo = serverInfo.replace("\r","").split("\n")
    while serverInfo[-1] == "":
        serverInfo.pop(-1)

    jsonDataDict = {}
    jsonDataDict["name"] = serverInfo[0]
    jsonDataDict["version"] = serverInfo[1]
    jsonDataDict["buildDate"] = serverInfo[2]

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