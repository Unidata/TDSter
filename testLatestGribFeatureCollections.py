import generateLatestReport
import os
import datetime as dt
import json
import io
from helpers.fileName_helper import getOutFilePath, getOutFileDataPath
from helpers.tdster_defaults import gribFeatureCollectionInfo, dateFormat


testing = False
outFilePath = ""
outFileDataPath = ""

def cleanFileName(fileName):
    fileName = fileName.replace(" ", "")
    fileName = fileName.replace(".","p")
    fileName = fileName.replace("(", "")
    fileName = fileName.replace(")", "")
    fileName = fileName.lower()

    return fileName

def testGribFeatureCollections(testServer, collectionName):
    global outFilePath
    global outFileDataPath
    global dateFormat

    print("Checking dataset age on {} for the {} collection".format(testServer, collectionName))

    scriptRunTime = dt.datetime.strftime(dt.datetime.utcnow(), dateFormat)

    if testServer[-1] != "/":
        testServer = testServer + "/"

    catalog = testServer + gribFeatureCollectionInfo[collectionName]["topCatalog"]
    # get full report on status for the given gribFeatureCollections
    fullReport = generateLatestReport.main(catalog)

    simpleAgeReport = fullReport["simpleAgeReport"]

    # read in json datafile, if it exists
    for reportName in simpleAgeReport:
        date_updated = False
        new_data = False

        reportFileName = cleanFileName(reportName) + ".json"

        outFileName = os.path.join(outFileDataPath, reportFileName)

        if os.path.exists(outFileName):
            # json file exists, read it in
            with io.open(outFileName, 'r', encoding='utf-8') as outfile:
              jsonDataDict = json.load(outfile)

            #collect known datasets in file
            # add the new scriptRunTime and data to the time data already present in file
            for reportName in simpleAgeReport:
                for colNum in range(len(jsonDataDict["columns"])):
                    if "date" in jsonDataDict["columns"][colNum] and not date_updated:
                        jsonDataDict["columns"][colNum].append(scriptRunTime)
                        date_updated = True
                    elif reportName in jsonDataDict["columns"][colNum]:
                        jsonDataDict["columns"][colNum].append(simpleAgeReport[reportName])
        else:
            # create a new data dictionary that has the
            # appropriate json format for D3 and C3 plotting
            # routines

            cols = []
            jsonDataDict = {}
            jsonDataDict["x"] = "date"
            cols.append(["date"] + [scriptRunTime])
            cols.append([reportName, simpleAgeReport[reportName]])
            jsonDataDict["columns"] = cols
            jsonDataDict["x_format"] = dateFormat

        # finally, write updated (or new) json data file for
        # the given dataset
        print("    Writing {} json data file".format(reportName))

        with io.open(outFileName, 'w', encoding='utf-8') as f:
          f.write(unicode(json.dumps(jsonDataDict, ensure_ascii=False)))
        f.close()

    return fullReport


def main(testServer):
    global outFilePath
    global outFileDataPath
    global testing
    for collectionName in gribFeatureCollectionInfo:
        outFileDataPath = getOutFileDataPath(testServer, testing)
        outFilePath = getOutFilePath(testServer, testing)

        fullReport = testGribFeatureCollections(testServer, collectionName)
        print("    Saving full age report")

        outFileName = os.path.join(outFileDataPath, "{}_fullReport.json".format(collectionName))

        with io.open(outFileName, 'w', encoding='utf-8') as f:
          f.write(unicode(json.dumps(fullReport, ensure_ascii=False)))
        f.close()

if __name__ == "__main__":
    from helpers.tdster_defaults import testServers
    for testServer in testServers:
        main(testServer)

