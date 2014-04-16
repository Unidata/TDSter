#
# Defaults for TDSter
#

def createGribFeatureCollectionInfo(testServers):
    coreFeatureCollectionInfo = {"ncep" : {"topCatalog" : "thredds/idd/modelsNcep.xml"},
                                 "fnmoc": {"topCatalog" : "thredds/idd/modelsFnmoc.xml"}}

    gribFeatureCollectionInfo = {}
    for testServer in testServers:
        gribFeatureCollectionInfo[testServer] = coreFeatureCollectionInfo.copy()
        #if "thredds-test.unidata.ucar.edu" in testServer:
        #    gribFeatureCollectionInfo[testServer]["gsd"] = {"topCatalog" : "thredds/modelsHrrr.xml"}

    return gribFeatureCollectionInfo



tmp_data_dir = '/Users/sarms/Desktop/tdsDashboard/tmpdir'
defaultTestCatalog = 'http://thredds-test.unidata.ucar.edu/thredds/modelsHrrr.xml'
testServers = ["http://thredds.ucar.edu/", "http://thredds-test.unidata.ucar.edu/"]
#testServers = ["http://thredds-test.unidata.ucar.edu/"]

gribFeatureCollectionInfo = createGribFeatureCollectionInfo(testServers)

dateFormat = "%Y-%m-%d %H%M"
#
# clean up some defaults to ensure conformity
#
