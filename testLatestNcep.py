import catalogTDS
from pydap.client import open_url
import dateutil.parser, dateutil.relativedelta
import pytz
import datetime as dt

def testLatestTime(catDataset):
    if catDataset.resolverUrl is not None:
        odapUrl = "http://thredds.ucar.edu/thredds/dodsC/" + catDataset.urlPath
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

            if timeDiff.days > 1:
                print("{} is off by more than {} day(s)!".format(catDataset.name, timeDiff.days))
            elif timeDiff.hours > 6:
                print("{} is off by more than {} hour(s)!".format(catDataset.name, timeDiff.hours))

ncepCatUrl = "http://thredds.ucar.edu/thredds/idd/modelsNcep.xml"

catalogTDS.applyTestFullCatalogInv(ncepCatUrl, datasetKey="latest", testFunc = testLatestTime)