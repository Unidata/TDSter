import catalogTDS
from pydap.client import open_url
import dateutil.parser, dateutil.relativedelta
import pytz
import datetime as dt
from helpers.tdster_defaults import testServer

report = []

def testLatestTime(catDataset):
    global report
    if catDataset.resolverUrl is not None:
        odapUrl = testServer + "thredds/dodsC/" + catDataset.urlPath
        timeVar = "time"
        dataset = open_url(odapUrl)
        initTimeVal = dataset[timeVar][0]
        timeUnits = dataset[timeVar].units

        # <TimeCount> since <isoString>
        if ((len(timeUnits.split(' ')) == 3) and (timeUnits.split(' ')[1] == "since")):
            offsetType = timeUnits.split(' ')[0].lower()
            baseTime = dateutil.parser.parse(timeUnits.split(' ')[-1])
            if "sec" in offsetType:
                timeOffsetFunct = lambda x : dateutil.relativedelta.relativedelta(secondss=x)
            elif "min" in offsetType:
                timeOffsetFunct = lambda x : dateutil.relativedelta.relativedelta(minutes=x)
            elif "hour" in offsetType:
                timeOffsetFunct = lambda x : dateutil.relativedelta.relativedelta(hours=x)
            elif "mon" in offsetType:
                timeOffsetFunct = lambda x : dateutil.relativedelta.relativedelta(months=x)

            initTime = baseTime + timeOffsetFunct(float(initTimeVal[0]))
            currentTime = dt.datetime.utcnow().replace(tzinfo=pytz.UTC)
            timeDiff = dateutil.relativedelta.relativedelta(currentTime, initTime)

            if timeDiff.days >= 1:
                report.append("The latest {} dataset is more than {} day(s) old!".format(catDataset.name, timeDiff.days))
            elif timeDiff.hours >= 12:
                report.append("The latest {} dataset is more than {} hours(s) old!".format(catDataset.name, timeDiff.hours))

def main(catalog):
    global report
    report = []

    catalogTDS.applyTestFullCatalogInv(catalog, datasetKey="latest", testFunc = testLatestTime)

    return report
