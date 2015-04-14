import config
import os
#
# Defaults for TDSter
#
confFileName = "Tdster.conf"
def findAndReadConfigFile():
   # first, check tld of TDSter
    conf = None
    found = False
    for loc in [os.path.expanduser("~/.unidata/TDSter"), os.environ.get("TDSTER_CONF")]:
        if not loc is None and not found:
            testConfFile = os.path.join(loc,confFileName)
            if os.path.isfile(testConfFile):
                conf = config.readConfig(testConfFile)
                found = True
    return conf

def createGribFeatureCollectionInfo(testServers):
    gribFeatureCollectionInfo = {}
    for testServer in testServers:
        if (("thredds.ucar.edu" in testServers) or ("weather.rsmas" in testServers)):
            coreFeatureCollectionInfo = {"ncep" : {"topCatalog" : "thredds/idd/modelsNcep.xml"},
                                         "fnmoc": {"topCatalog" : "thredds/idd/modelsFnmoc.xml"}}
        else:
            coreFeatureCollectionInfo = {"fpaa" : {"topCatalog" : "thredds/idd/forecastProdsAndAna.xml"},
                                         "fnmoc": {"topCatalog" : "thredds/idd/forecastModels.xml"}}

        gribFeatureCollectionInfo[testServer] = coreFeatureCollectionInfo.copy()

    return gribFeatureCollectionInfo

conf = findAndReadConfigFile()

tmp_data_dir = conf["tmpDataDir"]
defaultTestCatalog = 'http://thredds-test.unidata.ucar.edu/thredds/modelsHrrr.xml'
testServers = conf["testServers"]

gribFeatureCollectionInfo = createGribFeatureCollectionInfo(testServers)

dateFormat = conf["dateFormat"]
