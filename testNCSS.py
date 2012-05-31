import datetime as dt
import numpy as np
from string import join
from nose.tools import raises
from os import remove
from netCDF4 import Dataset
from TDSterErrors import NotAnNcFileError, MethodNotImplementedForFileType, UnexpectedFileTypeReturn
from urllib2 import HTTPError

class NcssData(object):
    def __init__(self, base_url, ncss_request, return_file, return_file_type):
        self.base_url = base_url
        self.ncss_request = ncss_request
        self.return_file = return_file

        if return_file_type != '':
            self.return_file_type = return_file_type
        else:
            self.return_file_type = 'netcdf'

        self.data = {}
        self.data_set = {'any' : False}

    def read_data(self,var):
        #
        #open netCDF file from subset
        #
        if self.return_file_type == 'netcdf':
            try:
                ncf = Dataset(self.return_file, 'r')
            except RuntimeError:
                raise NotAnNcFileError(self.return_file)

            self.data[var] = ncf.variables[var][:]

            if self.data_set['any']:
                self.data_set['any'] = True

            self.data_set[var] = True
            ncf.close()
        else:
            #
            # check to see if netCDF file was returned even though we asked for this not to happen!
            #
            try:
                ncf = Dataset(self.return_file, 'r')
                raise UnexpectedFileTypeReturn(self, received = 'netcdf')
            except RuntimeError:
                pass #we expect this to fail
            except UnexpectedFileTypeReturn, e:
                print e.__str__()
                print "NCSS url: {}".format(self.base_url + self.ncss_request)
                raise

            raise MethodNotImplementedForFileType(method = 'read_data', file_type = self.return_file_type)

    def remove_return_file(self):
        #
        # delete the temporary netCDF file
        #
        remove(self.return_file)

    def check_against_odap(self, odap_data, var, squeeze = True, odap_subset = None):
        odap_data_ = odap_data[var][var][:]
        if odap_subset is not None:
            odap_data_ = eval('odap_data_[{}]'.format(odap_subset))

        if not self.data_set.has_key(var):
            self.read_data(var)

        try:
            if squeeze:
                assert np.all(self.data[var].squeeze() == odap_data_)
            else:
                assert np.all(self.data[var] == odap_data_)
        except AssertionError:
            if squeeze:
                diff = self.data[var].squeeze() - odap_data_
            else:
                diff = self.data[var] - odap_data
            print "The data returned from the netCDF Subset Service does not match the expected data based data from the OpENDAP Service\n"
            print "The average magnitude of the difference between the two datasets is: {}\n".format(np.abs(diff).mean())
            print "NCSS url: {}".format(self.base_url + self.ncss_request)
            raise

    def check_subset_basic(self, odap_data, var, squeeze = True):
        odap_data_ = odap_data[var][var][:]

        if not self.data_set.has_key(var):
            self.read_data(var)

        try:
            if squeeze:
                assert self.data[var].squeeze().shape != odap_data_.shape
            else:
                assert self.data[var].shape != odap_data_.shape

        except AssertionError:
            print "Based on the shape of the datasets returned from the netCDF Subset Service, no subsetting was performed\n"
            print "Full dataset shape: {}\n".format(odap_data_.shape)
            if squeeze:
                print "Subset dataset shape: {}\n".format(self.data[var].squeeze().shape)
            else:
                print "Subset dataset shape: {}\n".format(self.data[var].shape)
            print "NCSS url: {}".format(self.base_url + self.ncss_request)
            raise

def get_odap_data(requested_vars, data_url = None):
    from helpers import get_data_url, url_service_transform
    from pydap.client import open_url

    if data_url is None:
        odap_url = get_data_url(service = 'odap')
    else:
        odap_url = url_service_transform(url, to_service = 'odap')

    dataset = open_url(odap_url)

    user_vars = {}
    for var in requested_vars:
        user_vars[var] = dataset[var]
    
    return user_vars

def get_ncss_request(basic_ncss_request, kind = '', return_type = '', addLatLon = False):

    ncss_request = basic_ncss_request

    if kind == 'grid_as_point':
        ncss_request = (join([ncss_request,'point=true'],sep='&'))

    if return_type != '':
        ncss_request = (join([ncss_request,join(['accept',return_type],sep='=')],sep='&'))

    if addLatLon:
        ncss_request = join([ncss_request,'addLatLon=True'],'&')

    return ncss_request

def get_ncss_data(basic_ncss_request='', dataset = 'NCEP_NAM_CONUS_80km', age = 'latest', service = 'ncss',
                  kind = '', return_file_type = '', addLatLon = False):
    import urllib2
    import os.path
    from helpers import get_data_url


    ncss_request = get_ncss_request(basic_ncss_request, kind = kind, return_type = return_file_type,
                                    addLatLon = addLatLon)

    base_url = get_data_url(dataset = dataset, age = age, service = service)

    full_url = join([base_url,ncss_request],'')
    # Request the data and store them in a tmp file
    url_request = urllib2.Request(full_url)
    url_request.add_header('User-agent', 'pyTDSter')
    try:
        response = urllib2.urlopen(url_request)
    except IOError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: {}'.format(e.reason)
            raise
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: {}'.format(e.code)
            print 'TDS response: {}'.format(e.read())
            print 'Full  url: {}'.format(full_url)
            raise
        else:
            print 'error not caught!'
            raise
    data_info = response.readlines()

    if ((return_file_type == 'netcdf') or (return_file_type == '')):
        return_file = os.path.join('data_tmp','tmp.nc')
    elif (return_file_type == 'csv'):
        return_file = os.path.join('data_tmp','tmp.csv')
    elif (return_file_type == 'xml'):
        return_file = os.path.join('data_tmp','tmp.xml')

    return_file = os.path.relpath(return_file)
    return_file = os.path.abspath(return_file)

    f = open(return_file, 'w')
    for line in data_info:
        f.write(line)
    f.close()

    #
    # Initialize and return a NcssData object
    #
    return NcssData(base_url, ncss_request, return_file, return_file_type)

################
# Test Section #
################

##############################################
# NetCDF Subset Service for Gridded Datasets #
##############################################

def test_ncss_var():
    # Request data via ncss
    var = 'Temperature_height_above_ground'
    basic_ncss_request = "?var={}&temporal=all".format(var)
    ncss = get_ncss_data(basic_ncss_request = basic_ncss_request, service = 'ncss')
    # get data via opendap
    odap_data = get_odap_data([var,])
    # data from variables obtained via opendap and ncss should be the same
    ncss.check_against_odap(odap_data, var)
    ncss.remove_return_file()

def test_ncss_var_specify_return_netcdf():
    # Request data via ncss
    var = 'Temperature_height_above_ground'
    basic_ncss_request = "?var={}&temporal=all".format(var)
    ncss = get_ncss_data(basic_ncss_request = basic_ncss_request, service = 'ncss', return_file_type = 'netcdf')
    # get data via opendap
    odap_data = get_odap_data([var,])
    # data from variables obtained via opendap and ncss should be the same
    ncss.check_against_odap(odap_data, var)
    ncss.remove_return_file()

@raises(HTTPError)
def test_ncss_var_specify_return_csv():
    # Request data via ncss
    var = 'Temperature_height_above_ground'
    basic_ncss_request = "?var={}".format(var)
    ncss = get_ncss_data(basic_ncss_request = basic_ncss_request, service = 'ncss', return_file_type = 'csv')
    ncss.remove_return_file()

@raises(HTTPError)
def test_ncss_var_specify_return_xml():
    # Request data via ncss
    var = 'Temperature_height_above_ground'
    basic_ncss_request = "?var={}".format(var)
    ncss = get_ncss_data(basic_ncss_request = basic_ncss_request, service = 'ncss', return_file_type = 'xml')
    ncss.remove_return_file()

#
# We expect this to fail with the AssertionError, so we use the
# @raises decorator of nose to say "it's cool, we know and, right now,
# expect this to happen"
#
@raises(NotAnNcFileError)
def test_ncss_var_lat_lon():
    # Request data via ncss
    var = 'Temperature_height_above_ground'
    lat = 40
    lon = -104
    ncss = get_ncss_data(basic_ncss_request =
    "?var={}&latitude={}&longitude={}".format(var,lat,lon), service = 'ncss')
    # get data via opendap
    odap_data = get_odap_data([var,])
    # Check if subsetting done (shapes should be different) Note: this
    #  does not check if subsetting done correctly!
    ncss.check_subset_basic(odap_data, var)
    ncss.remove_return_file()

def test_ncss_var_lat_lon_bounding_box():
    # Request data via ncss
    var = 'Temperature_height_above_ground'
    lat = 40
    lon = -104
    delta = 2.3
    ncss = get_ncss_data(basic_ncss_request =
    "?var={}&north={}&west={}&east={}&south={}".format(var,
        lat + delta,
        lon - delta,
        lon + delta,
        lat - delta),
        service = 'ncss')
    # get data via opendap
    odap_data = get_odap_data([var,])
    # Check if subsetting done (shapes should be different) Note: this
    #  does not check if subsetting done correctly!
    ncss.check_subset_basic(odap_data, var)
    ncss.remove_return_file()

def test_ncss_var_coordinate_bounding_box():
    # Request data via ncss
    var = 'Temperature_height_above_ground'
    minx=-10
    maxx=10
    miny=-4015
    maxy=-4000
    ncss = get_ncss_data(basic_ncss_request =
    "?var={}&minx={}&miny={}&maxx={}&maxy={}".format(var,
        minx,
        miny,
        maxx,
        maxy),
        service = 'ncss', dataset='NCEP_DGEX_AK_12km')
    # get data via opendap
    #odap_data = get_odap_data([var,])
    # Check if subsetting done (shapes should be different) Note: this
    #  does not check if subsetting done correctly!
    #ncss.check_subset_basic(odap_data, var)
    ncss.remove_return_file()

def test_ncss_var_all_spatial_subset():
    # Request data via ncss
    var = 'all'
    lat = 40
    lon = -104
    delta = 2.3
    ncss = get_ncss_data(basic_ncss_request =
    "?var={}&north={}&west={}&east={}&south={}".format(var,
        lat + delta,
        lon - delta,
        lon + delta,
        lat - delta),
        service = 'ncss')
    # get data via opendap
    #odap_data = get_odap_data([var1,var2])
    # Check if subsetting done (shapes should be different) Note: this
    #  does not check if subsetting done correctly!
    #ncss.check_subset_basic(odap_data, var1)
    #ncss.check_subset_basic(odap_data, var2)
    ncss.remove_return_file()

def test_ncss_dub_var_bounding_box():
    # Request data via ncss
    var1 = 'Temperature_height_above_ground'
    var2 = 'Relative_humidity_height_above_ground'
    var = join([var1,var2],',')
    lat = 40
    lon = -104
    delta = 2.3
    ncss = get_ncss_data(basic_ncss_request =
    "?var={}&north={}&west={}&east={}&south={}".format(var,
        lat + delta,
        lon - delta,
        lon + delta,
        lat - delta),
        service = 'ncss')
    # get data via opendap
    odap_data = get_odap_data([var1,var2])
    # Check if subsetting done (shapes should be different) Note: this
    #  does not check if subsetting done correctly!
    ncss.check_subset_basic(odap_data, var1)
    ncss.check_subset_basic(odap_data, var2)
    ncss.remove_return_file()

def test_ncss_var_single_time():
    # Request data via ncss
    from helpers import get_init_time
    init_time = get_init_time()
    var = 'Temperature_height_above_ground'
    ncss = get_ncss_data(basic_ncss_request =
    "?var={}&time={}".format(var, init_time.strftime('%Y-%m-%dT%H:%MZ')),
        service='ncss')
    # get data via opendap
    odap_data = get_odap_data([var,])
    # Check if subsetting done (shapes should be different) Note: this
    #  does not check if subsetting done correctly!
    ncss.check_subset_basic(odap_data, var)
    # Check if subsetting is done correctly!
    ncss.check_against_odap(odap_data, var, odap_subset = '0,:')
    ncss.remove_return_file()

def test_ncss_var_single_time_present():
    # Request data via ncss
    var = 'Temperature_height_above_ground'
    ncss = get_ncss_data(basic_ncss_request =
    "?var={}&time={}".format(var, 'present'), service='ncss')
    # get data via opendap
    odap_data = get_odap_data([var,])
    # Check if subsetting done (shapes should be different) Note: this
    #  does not check if subsetting done correctly!
    ncss.check_subset_basic(odap_data, var)
    # \\ToDo Check if subsetting is done correctly!
    #ncss.check_against_odap(odap_data, var, odap_subset = '0,:,:,:')
    ncss.remove_return_file()

def test_ncss_var_time_range():
    from helpers import get_init_time, get_time_offset
    # Request data via ncss
    init_time = get_init_time()
    time_index = 2
    end_time = init_time + get_time_offset(time_index)
    var = 'Temperature_height_above_ground'
    ncss = get_ncss_data(basic_ncss_request =
    "?var={}&time_start={}&time_end={}".format(var,
        init_time.strftime('%Y-%m-%dT%H:%MZ'),
        end_time.strftime('%Y-%m-%dT%H:%MZ')),
        service='ncss')
    # get data via opendap
    odap_data = get_odap_data([var,])
    # Check if subsetting done (shapes should be different) Note: this
    #  does not check if subsetting done correctly!
    ncss.check_subset_basic(odap_data, var)
    # Check if subsetting is done correctly!
    ncss.check_against_odap(odap_data, var, odap_subset = '0:{},:'.format(time_index+1))
    ncss.remove_return_file()

def test_ncss_var_time_duration_after_present():
    # Request data via ncss
    var = 'Temperature_height_above_ground'
    ncss = get_ncss_data(basic_ncss_request =
    "?var={}&time_start={}&time_duration={}".format(var,
        'present',
        'P1D'),
        service='ncss')
    # get data via opendap
    odap_data = get_odap_data([var,])
    # Check if subsetting done (shapes should be different) Note: this
    #  does not check if subsetting done correctly!
    ncss.check_subset_basic(odap_data, var)
    ncss.remove_return_file()

def test_ncss_var_time_duration_before_present():
    # Request data via ncss
    var = 'Temperature_height_above_ground'
    ncss = get_ncss_data(basic_ncss_request =
    "?var={}&time_start={}&time_duration={}".format(var,
        'present',
        'PT6H'), service='ncss')
    # get data via opendap
    odap_data = get_odap_data([var,])
    # Check if subsetting done (shapes should be different) Note: this
    #  does not check if subsetting done correctly!
    ncss.check_subset_basic(odap_data, var)
    ncss.remove_return_file()

@raises(HTTPError)
def test_ncss_file_size_limit():
    #
    # Should fail as this is over the MaxFileDownloadSize Limit
    #
    # Request data via ncss
    var = join(['Dew-point_temperature_height_above_ground',
                'Relative_humidity_height_above_ground',
                'Temperature_height_above_ground'],',')
    ncss = get_ncss_data(basic_ncss_request =
        "?var={}&temporal=all".format(var),
        service='ncss', dataset='NCEP_NAM_CONUS_12km')
    # get data via opendap
    ncss.remove_return_file()

####################################################
# NetCDF Subset Service for Grid as Point Datasets #
####################################################

def test_ncss_gasp_var_netCDF():
    # Request data via ncss
    var = 'Temperature_height_above_ground'
    basic_ncss_request = "?var={}".format(var)
    ncss = get_ncss_data(basic_ncss_request = basic_ncss_request, service = 'ncss', kind='grid_as_point',
                         return_file_type = 'netcdf')
    ncss.remove_return_file()

def test_ncss_gasp_var_lat_lon_netCDF():
    # Request data via ncss
    var = 'Temperature_height_above_ground'
    lat = 40
    lon = -104
    basic_ncss_request = "?var={}&latitude={}&longitude={}".format(var,lat,lon)
    ncss = get_ncss_data(basic_ncss_request = basic_ncss_request, service = 'ncss', kind='grid_as_point',
                         return_file_type = 'netcdf',  addLatLon = True)
    # get data via opendap
    odap_data = get_odap_data([var,])
    # Check if subsetting done (shapes should be different) Note: this
    #  does not check if subsetting done correctly!
    ncss.check_subset_basic(odap_data, var)
    # ToDo: Check if subsetting is done correctly!
    #ncss.check_against_odap(odap_data, var, odap_subset = ':,{},{}'.format(time_index+1))
    ncss.remove_return_file()

def test_ncss_var_single_time_netCDF():
    # Request data via ncss
    from helpers import get_init_time
    init_time = get_init_time()
    var = 'Temperature_height_above_ground'
    lat = 40
    lon = -104
    basic_ncss_request = "?var={}&latitude={}&longitude={}&time={}".format(var,lat,lon,init_time.strftime('%Y-%m-%dT%H:%MZ'))
    ncss = get_ncss_data(basic_ncss_request = basic_ncss_request, service = 'ncss', kind='grid_as_point',
        return_file_type = 'netcdf')
    # get data via opendap
    odap_data = get_odap_data([var,])
    # Check if subsetting done (shapes should be different) Note: this
    #  does not check if subsetting done correctly!
    ncss.check_subset_basic(odap_data, var)
    # ToDo: Check if subsetting is done correctly!
    #ncss.check_against_odap(odap_data, var, odap_subset = ':,{},{}'.format(time_index+1))
    ncss.remove_return_file()

def test_ncss_var_single_time_present_netCDF():
    # Request data via ncss
    var = 'Temperature_height_above_ground'
    lat = 40
    lon = -104
    basic_ncss_request = "?var={}&latitude={}&longitude={}&time={}".format(var,lat,lon,'present')
    ncss = get_ncss_data(basic_ncss_request = basic_ncss_request, service = 'ncss', kind='grid_as_point',
        return_file_type = 'netcdf')
    # get data via opendap
    odap_data = get_odap_data([var,])
    # Check if subsetting done (shapes should be different) Note: this
    #  does not check if subsetting done correctly!
    ncss.check_subset_basic(odap_data, var)
    # ToDo: Check if subsetting is done correctly!
    #ncss.check_against_odap(odap_data, var, odap_subset = ':,{},{}'.format(time_index+1))
    ncss.remove_return_file()

############################
# TDS Service Sanity Check #
############################

