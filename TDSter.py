def run_ncss_tests():
    import os
    # check for tmp data dir for NCSS tests
    tmp_data_dir = '.data_tmp/'
    if !os.path.exists(tmp_data):
        os.mkdir(tmp_data_dir)

    os.system('nosetests testNCSS.py --verbosity=1 --nologcapture')

if __name__ == '__main__':
    run_ncss_tests()