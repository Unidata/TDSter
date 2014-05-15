import generateLatestReport
import os
import datetime as dt
import json
import io
from helpers.fileName_helper import getOutFilePath, getOutFileDataPath

dateFormat = "%Y-%m-%d %H%M"
outFilePath = ""
outFileDataPath = ""

def test_ncep_latest(testServer):
    global outFilePath
    global outFileDataPath

    print("Checking dataset age on {}".format(testServer))

    scriptRunTime = dt.datetime.strftime(dt.datetime.utcnow(), dateFormat)

    if testServer[-1] != "/":
        testServer = testServer + "/"

    catalog = testServer + "thredds/idd/modelsNcep.xml"
    fullReport = generateLatestReport.main(catalog)

    simpleAgeReport = fullReport["simpleAgeReport"]

    datasetNames = {"DGEX" : "dgex.json",
                    "GEFS": "gefs.json",
                    "GFS": "gfs.json",
                    "NAM": "nam.json",
                    "National Digital Forecast Database": "ndfd.json",
                    "Real Time Mesoscale Analysis": "rtma.json",
                    "Rapid Refresh": "rap.json",
                    "SREF": "sref.json",
                    "Wave Watch III": "ww3.json",}

    def initNames():
        dataDict = {}
        for name in datasetNames:
            dataDict[name] = {}
        return dataDict

    # read in json datafile, if it exists
    for name in datasetNames:
        date_updated = False

        outFileName = os.path.join(outFileDataPath, datasetNames[name])

        if os.path.exists(outFileName):
          with io.open(outFileName, 'r', encoding='utf-8') as outfile:
            jsonDataDict = json.load(outfile)

            for key in simpleAgeReport:
                for colNum in range(len(jsonDataDict["columns"])):
                    if key in jsonDataDict["columns"][colNum]:
                        jsonDataDict["columns"][colNum].append(simpleAgeReport[key])
                    elif "date" in jsonDataDict["columns"][colNum] and not date_updated:
                        jsonDataDict["columns"][colNum].append(scriptRunTime)
                        date_updated= True
        else:
            dataDict = initNames()
            for key in simpleAgeReport:
                if key.rfind(name) > 0:
                    if dataDict.has_key(key):
                        dataDict[name][key].append(simpleAgeReport[key])
                    else:
                        dataDict[name][key] = []
                        dataDict[name][key].append(simpleAgeReport[key])
            jsonDataDict = {}
            jsonDataDict["x"] = "date"
            cols = []
            cols.append(["date"] + [scriptRunTime])
            for colName in dataDict[name]:
                cols.append([colName] + dataDict[name][colName])
            jsonDataDict["columns"] = cols
            jsonDataDict["x_format"] = dateFormat

        print("    Writing {} json data file".format(name))

        with io.open(outFileName, 'w', encoding='utf-8') as f:
          f.write(unicode(json.dumps(jsonDataDict, ensure_ascii=False, indent=2)))

    return fullReport


def main(testServer):
    global outFilePath
    global outFileDataPath

    outFileDataPath = getOutFileDataPath(testServer)
    outFilePath = getOutFilePath(testServer)

    fullReport = test_ncep_latest(testServer)
    print("    Saving full age report")

    outFileName = os.path.join(outFilePath, "data", "fullReport.json")

    with io.open(outFileName, 'w', encoding='utf-8') as f:
      f.write(unicode(json.dumps(fullReport, ensure_ascii=False, indent=2)))

if __name__ == "__main__":
    from helpers.tdster_defaults import testServers
    for testServer in testServers:
        main(testServer)

