from http_helper import get_user_agent
from tdster_defaults import testServer

__all__ = ['strip_date', 'get_data_url', 'url_service_transform']


def strip_date(x):
    '''
    A method to skip reading the date string from the datafile
    by simply returning -999 for that column of information.
    '''
    return -999

def url_service_transform(url, from_service = None, to_service = None):
    from TDSterErrors import NotAValidService
    service_id = {'ncss' : '/ncss/grid/',
                  'odap' : '/dodsC/',
                  'catalog' : '/catalog/',
                  'cdmremote' : '/cdmremote/',
                  'http' : '/fileServer/',
                  'wms' : '/wms/',
                  'wcs' : '/wcs/',
                  'iso' : '/iso/',
                  'uddc' : '/uddc/',
                  'ncml' : '/ncml/'
                 }
    if (to_service is None) or (to_service not in service_id.keys()):
        valid_services = service_id.keys()
        raise NotAValidService(valid_services, to_service)

    if (from_service is not None) and (to_service is not None):
        return url.replace(service_id[from_service], service_id[to_service])
    elif (from_service is None):
        for service in service_id:
            if service_id[service] in url:
                return url.replace(service_id[service], service_id[to_service])

def get_data_url(dataset = 'NCEP_NAM_CONUS_80km', age = 'latest', service = 'ncss', server='4.3'):

    '''
    This function is used to retrieve the url on the motherlode
    THREDDS server for the latest NAM12 model run.

    Parameters
    ----------
    kind : string [odap, ncss]
        A string that describes the type of access service the user 
        wishes to use. Must be 'odap' or 'ncss'
    grid_kind : string [grid, point]
        A string that indicates which view of a gridded dataset to subset: the
        grid, or the grid as a point

    Returns
    -------
    data_url : string
        The URL that points to the datafile using the specified protocol.
    '''
    import urllib2
    import random
    from string import join

    top_level_data_urls = {
        'NCEP_GEFS_GLOBAL_1deg' : join([testServer,'thredds/ncss/grid/grib/NCEP/GEFS/Global_1p0deg_Ensemble/members/best'],'/'),
        'NCEP_NAM_CONUS_80km' : join([testServer,'thredds/catalog/grib/NCEP/NAM/CONUS_80km/files/catalog.html'],'/'),
        'NCEP_NAM_AK_95km' : join([testServer,'thredds/catalog/grib/NCEP/NAM/Alaska_95km/files/catalog.html'],'/'),
        'NCEP_NAM_CONUS_12km'  : join([testServer,'thredds/catalog/grib/NCEP/NAM/CONUS_12km/conduit/files/catalog.html'],'/'),
        'NCEP_DGEX_AK_12km' : join([testServer, 'thredds/catalog/grib/NCEP/DGEX/Alaska_12km/files/catalog.html'],'/'),
    }

    if '/best' not in top_level_data_urls[dataset]:
        links_to_data_url = top_level_data_urls[dataset]

        url_request = urllib2.Request(links_to_data_url)
        url_request.add_header('User-agent', get_user_agent())

        ava_data = urllib2.urlopen(url_request)

        # collect all links on the page
        data_links = []
        for line in ava_data:
            if ('<a href' in line) and ('catalog.html?' in line) and ('img src' not in line):
                data_links.append(line)

        ava_data.close()
        tmp_data_url_index = None
        if age == 'latest':
            tmp_data_url_index = 0
        elif age == 'random':
            tmp_data_url_index = random.randrange(0,len(data_links),1)


        tmp_data_url = data_links[tmp_data_url_index].split("'")[1].split('=')[1]
        base_data_url = join([testServer,'thredds','catalog',tmp_data_url],'/')
        data_url = url_service_transform(base_data_url, from_service = 'catalog', to_service = service)

    else:
        data_url = top_level_data_urls[dataset]

    return data_url
