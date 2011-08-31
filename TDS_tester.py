import testNCSS as ncss
from string import join

def test_ncss_var():
    var = 'Temperature_height_above_ground'
    passed = ncss.check_ncss(data_request_string =
             "?var={}".format(var))
    assert passed == True

def test_ncss_var_lat_lon():
    var = 'Temperature_height_above_ground'
    lat = 40
    lon = -104
    passed = ncss.check_ncss(data_request_string =
             "?var={}&latitude={}&longitude={}".format(var,lat,lon))
    assert passed == True

def test_ncss_var_bounding_box():
    var = 'Temperature_height_above_ground'
    lat = 40
    lon = -104
    delta = 2.3
    passed = ncss.check_ncss(data_request_string =
    "?var={}&spatial=bb&north={}&west={}&east={}&south={}".format(var,
                                                           lat + delta,
                                                           lon - delta,
                                                           lon + delta,
                                                           lat - delta))
    assert passed == True

def test_ncss_dub_var_bounding_box():
    var1 = 'Temperature_height_above_ground'
    var2 = 'Pressure_reduced_to_MSL'
    var = join([var1,var2],',')
    lat = 40
    lon = -104
    delta = 2.3
    passed = ncss.check_ncss(data_request_string =
    "?var={}&spatial=bb&north={}&west={}&east={}&south={}".format(var,
                                                           lat + delta,
                                                           lon - delta,
                                                           lon + delta,
                                                           lat - delta))
    assert passed == True

def test_ncss_var_single_time():
    from helpers import get_init_time
    init_time = get_init_time()
    var = 'Temperature_height_above_ground'
    passed = ncss.check_ncss(data_request_string =
             "?var={}&time={}".format(var, init_time))
    assert passed == True

def test_ncss_var_time_range():
    from helpers import get_init_time
    init_time = get_init_time()
    end_time = init_time
    var = 'Temperature_height_above_ground'
    passed = ncss.check_ncss(data_request_string =
             "?var={}&time={}".format(var, init_time))
    assert passed == True

if __name__ == '__main__':
    import os
    os.system('nosetests TDS_tester.py')
