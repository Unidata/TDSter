dataDir = ""

def getOutFilePath(serverUrl, test = False):
    import os
    global dataDir

    initDataDir(test)

    outFilePath = os.path.join(dataDir, getServerUrlAsString(serverUrl))
    if not os.path.exists(outFilePath):
        os.mkdir(outFilePath)
    return outFilePath

def getOutFileDataPath(serverUrl, test = False):
    import os
    global dataDir

    initDataDir(test)

    topLevelOutFilePath = getOutFilePath(serverUrl, test)
    outFilePath = os.path.join(topLevelOutFilePath, "data")
    if not os.path.exists(outFilePath):
        os.mkdir(outFilePath)
    return outFilePath

def getServerUrlAsString(serverUrl):
    return serverUrl.replace("http",'').replace('.','-').replace('/','').replace(":","")

def initDataDir(test = False):
    global dataDir
    dataDirMain = "/Users/sarms/Desktop/tdsDashboard/reports"
    dataDirTest = "/Users/sarms/Desktop/tdsDashboard/reportsTest"
    import os

    if not test:
        dataDir = os.path.join(dataDirMain)
    else:
        dataDir = os.path.join(dataDirTest)

    if not os.path.exists(dataDir):
        os.mkdir(dataDir)

