import catalogTDS
from pydap.client import open_url
from pydap.exceptions import ServerError
import dateutil.parser, dateutil.relativedelta
import pytz
import datetime as dt
from dateutil import parser

from helpers.tdster_defaults import testServer

potentialStaleDSReport = {}
simpleAgeReport = {}
latestUrlReport = {}


def testLatestTimeByName(catDataset):
    global potentialStaleDSReport
    global simpleAgeReport
    global latestUrlReport

    if catDataset.resolverUrl is not None:
        fileName = catDataset.urlPath
        latestUrlReport[catDataset.name] = catDataset.accessUrls
        fullTime = fileName.split("_")
        fileDate = fullTime[-2]
        fileTime = fullTime[-1].split('.')[0]
        initTime = parser.parse(fileDate + fileTime).replace(tzinfo=pytz.UTC)
        currentTime = dt.datetime.utcnow().replace(tzinfo=pytz.UTC)
        timeDiff = dateutil.relativedelta.relativedelta(currentTime, initTime)
        simpleAgeReport[catDataset.name] = timeDiff.hours
        if timeDiff.hours < 0:
            print("help - time diff is negative: {} hours".format(timeDiff.hours))
        if timeDiff.hours >= 12:
            message = "The latest {} dataset is more than {} hours(s) old!".format(catDataset.name, timeDiff.hours)
            potentialStaleDSReport[catDataset.name] = message



def main(catalog):
    global potentialStaleDSReport
    potentialStaleDSReport = {}
    global simpleAgeReport
    simpleAgeReport = {}
    global latestUrlReport
    latestUrlReport = {}

    catalogTDS.applyTestFullCatalogInv(catalog, datasetKey="latest", testFunc = testLatestTimeByName)
    #catalogTDS.applyTestFullCatalogInv(catalog, datasetKey="latest")
    #for key in fullReport:
    #    print("{}, {}".format(key, fullReport[key]))

    fullReport = {"simpleAgeReport" : simpleAgeReport,
                  "potentialStaleDSReport" : potentialStaleDSReport,
                  "latestUrlReport" : latestUrlReport
                  }
    return fullReport
