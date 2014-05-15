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
    fileName = fileName.replace("latestreferencetimecollectionfor", "latest")

    return fileName

def testGribFeatureCollections(testServer, collectionName):
    global outFilePath
    global outFileDataPath
    global dateFormat

    print("Checking dataset age on {} for the {} collection".format(testServer, collectionName))

    scriptRunTime = dt.datetime.strftime(dt.datetime.utcnow(), dateFormat)

    if testServer[-1] != "/":
        testServer = testServer + "/"

    catalog = testServer + gribFeatureCollectionInfo[testServer][collectionName]["topCatalog"]
    # get full report on status for the given gribFeatureCollections
    fullReport = generateLatestReport.main(catalog)

    simpleAgeReport = fullReport["simpleAgeReport"]

    # read in json datafile, if it exists
    for newReportName in simpleAgeReport:
        date_updated = False

        reportFileName = cleanFileName(newReportName) + ".json"

        outFileName = os.path.join(outFileDataPath, reportFileName)

        if os.path.exists(outFileName):
            # json file exists, read it in
            with io.open(outFileName, 'r', encoding='utf-8') as outfile:
              jsonDataDict = json.load(outfile)

            #collect known datasets in file
            # add the new scriptRunTime and data to the time data already present in file
            for reportName in simpleAgeReport:
                # look for reportName in the file - must loop through all cols to see if
                # it is anywhere in there
                for colNum in range(len(jsonDataDict["columns"])):
                    # if the data entry is for the date, update it once and do not
                    # check again
                    if "date" in jsonDataDict["columns"][colNum] and not date_updated:
                        jsonDataDict["columns"][colNum].append(scriptRunTime)
                        date_updated = True
                    # look for the correct data entry for reportName
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
            cols.append([newReportName, simpleAgeReport[newReportName]])
            jsonDataDict["columns"] = cols
            jsonDataDict["x_format"] = dateFormat

        # finally, write updated (or new) json data file for
        # the given dataset
        print("    Writing {} json data file".format(newReportName))

        with io.open(outFileName, 'w', encoding='utf-8') as f:
          f.write(unicode(json.dumps(jsonDataDict, ensure_ascii=False, indent=2)))
        f.close()

    return fullReport


def main(testServer):
    global outFilePath
    global outFileDataPath
    global testing
    for collectionName in gribFeatureCollectionInfo[testServer]:
        outFileDataPath = getOutFileDataPath(testServer, testing)
        outFilePath = getOutFilePath(testServer, testing)

        fullReport = testGribFeatureCollections(testServer, collectionName)
        print("    Saving full age report")

        outFileName = os.path.join(outFileDataPath, "{}_fullReport.json".format(collectionName))

        with io.open(outFileName, 'w', encoding='utf-8') as f:
          f.write(unicode(json.dumps(fullReport, ensure_ascii=False, indent=2)))
        f.close()

if __name__ == "__main__":
    from helpers.tdster_defaults import testServers
    for testServer in testServers:
        main(testServer)

