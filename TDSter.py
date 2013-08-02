def run_tests(verbosity=1):
    import os
    from string import join
    from helpers import tdster_defaults
    # check for tmp data dir for NCSS tests

    if not os.path.exists(tdster_defaults.tmp_data_dir):
        os.mkdir(tdster_defaults.tmp_data_dir)

    tests = join(['testServiceSanity.py',
                  'testNCSS.py',
                  'testMotherlodeTopcatalog.py',
                  'testLatestNcep.py',
                  'testLatestFnmoc.py'], ',')

    nosetests_options = join(['--tests={}'.format(tests),
                              '--verbosity={}'.format(verbosity),
                              '--nologcapture'], ' ')

    os.system('nosetests {}'.format(nosetests_options,))

    os.removedirs(tdster_defaults.tmp_data_dir)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Run the THREDDS DATA SERVER test suite")
    parser.add_argument("-v", "--verbosity", type=int, default=1,
                        help="controls output detail level from nosetests [1-10; default 1 (minimal details)]")
    args = parser.parse_args()

    run_tests(verbosity=args.verbosity)

