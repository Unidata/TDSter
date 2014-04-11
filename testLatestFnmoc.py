import generateLatestReport
from TDSterErrors import StaleDatasetsDetected

def test_fnmoc_latest():

    from helpers.tdster_defaults import testServer
    if testServer[-1] != "/":
        testServer = testServer + "/"

    catalog = testServer + "thredds/idd/modelsFnmoc.xml"

    report = generateLatestReport.main(catalog)

    try:
        assert len(report) == 0
    except AssertionError:
        raise StaleDatasetsDetected(report)

if __name__ == "main":
    test_fnmoc_latest()
