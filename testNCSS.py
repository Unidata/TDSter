class NotAnNCFileError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def check_ncss(data_request_string=''):
    import os
    import urllib2
    from helpers import strip_date, get_latest_nam80_url

    is_nc = True
    # get the url of the latest NAM80 model run
    ncss_url = get_latest_nam80_url(service = 'ncss')
    # create string to request temperature data from the grid point
    #  closest to the given lat/long

    # Request the data and store them to a tmp file
    try:
        response = urllib2.urlopen(ncss_url + data_request_string)
        data_info = response.readlines()
        tmp_file = 'tmp.nc'
        f = open(tmp_file, 'w')
        for line in data_info:
            f.write(line)
        f.close()

        is_nc = os.system('ncdump -h tmp.nc | grep Temperature_height_above_ground >> /dev/null')
        os.remove('tmp.nc')
    except urllib2.HTTPError:
        print('{} is not a valid NCSS request, or file {} does not exist on the server'.format(data_request_string, ncss_url.split('/')[-1]))
        raise
    # is_nc = 0 for command completed successfully
    # is_nc != 0 for command failed
    # to make this a bool that makes sense, we must use not
    return not bool(is_nc)

#if __name__ == '__main__':
#    '''
#
#    This script uses the netCDF subservice feature of the THREDDS
#    data server to extract the timeseries output from a single grid
#    point in the latest NAM 12km run output. The grid point used
#    is chosen such that it is the closest to the zipcode entered
#    by the user.
#
#    '''
#    lat = 40.
#    lon = -104.
#
#    # get the url of the latest NAM12 model run
#    ncss_url = get_latest_nam12_url(kind = 'point')
#
#    # create string to request temperature data from the grid point
#    #  closest to the given lat/long
#    data_request_string = "?var=Temperature_surface&latitude={}&longitude={}&temporal=all&accept=csv&point=true".format(lat,lon)
#
#    # Request the data and store them to a tmp file
#    response = urllib2.urlopen(ncss_url + data_request_string)
#    data_info = response.readlines()
#    tmp_file = 'tmp.txt'
#    f = open(tmp_file, 'w')
#    for line in data_info:
#        f.write(line)
#    f.close()
