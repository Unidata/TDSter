def run_ncss_tests():
    import os
    os.system('nosetests testNCSS.py --verbosity=1 --nologcapture')

if __name__ == '__main__':
    run_ncss_tests()