﻿def run_tests(verbosity=1):
    import os
    # check for tmp data dir for NCSS tests
    tmp_data_dir = 'data_tmp/'
    if not os.path.exists(tmp_data_dir):
        os.mkdir(tmp_data_dir)

    os.system('nosetests --verbosity={} --nologcapture'.format(verbosity,))

    os.removedirs(tmp_data_dir)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Run the THREDDS DATA SERVER test suite")
    parser.add_argument("-v", "--verbosity", type=int, default=1,
                        help="controls output detail level from nosetests [1-10; default 1 (minimal details)]")
    args = parser.parse_args()

    run_tests(verbosity=args.verbosity)

