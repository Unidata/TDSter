def run_tests():
    import os
    from helpers import tdster_defaults
    import testLatestGribFeatureCollections
    import scrapeServerInfo
    import reportStaleDatasets
    tests = [testLatestGribFeatureCollections,
             scrapeServerInfo,
             reportStaleDatasets]

    for testServer in tdster_defaults.testServers:
        for tst in tests:
            mainMethod = '.main("{}")'.format(testServer)
            eval(tst.__name__ + mainMethod)
            print("")
        print("===============\n")

if __name__ == '__main__':
    #import argparse

    #parser = argparse.ArgumentParser(description="Run the THREDDS DATA SERVER test suite")
    #parser.add_argument("-v", "--verbosity", type=int, default=1,
    #                    help="controls output detail level from nosetests [1-10; default 1 (minimal details)]")
    #args = parser.parse_args()

    run_tests()

