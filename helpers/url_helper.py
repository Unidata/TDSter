__all__ = ['strip_date', 'get_data_url', 'url_service_transform']

def strip_date(x):
    '''
    A method to skip reading the date string from the datafile
    by simply returning -999 for that column of information.
    '''
    return -999

def url_service_transform(url, from_service = None, to_service = None):
    service_id = {'ncss' : '/ncss/grid/',
                  'odap' : '/dodsC/',
                  'catalog' : '/catalog/'
                 }
    if (from_service is not None) and (to_service is not None):
        return url.replace(service_id[from_service], service_id[to_service])
    elif (from_service is None):
        for service in service_id:
            if service_id[service] in url:
                return url.replace(service_id[service], service_id[to_service])

def get_data_url(dataset = 'NCEP_NAM_CONUS_80km', age = 'latest', service = 'ncss'):

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

    top_level_data_urls_4p2 = {
      'NCEP_NAM_CONUS_80km' : 'http://motherlode.ucar.edu/thredds/catalog/fmrc/NCEP/NAM/CONUS_80km/files/catalog.html',
      'NCAP_NAM_AK_95km' : 'http://motherlode.ucar.edu/thredds/catalog/fmrc/NCEP/NAM/Alaska_95km/files/catalog.html'
      }

    top_level_data_urls_4p3 = {
        'NCEP_NAM_CONUS_80km' : 'http://motherlode.ucar.edu:9080/thredds/catalog/grib/NCEP/NAM/CONUS_80km/LambertConformal-65X93-40p98N-100p0W/files/catalog.html',
        'NCAP_NAM_AK_95km' : 'http://motherlode.ucar.edu:9080/thredds/catalog/grib/NCEP/NAM/Alaska_95km/PolarStereographic-35X49-60p80N-149p1W/files/catalog.html'
    }

    top_level_data_urls = top_level_data_urls_4p3

    links_to_data_url = top_level_data_urls[dataset]

    ava_data = urllib2.urlopen(links_to_data_url)
    # collect all links on the page
    data_links = []
    for line in ava_data:
        if ('<a href' in line) and ('catalog.html?' in line) and ('img src' not in line):
            data_links.append(line)

    ava_data.close()

    if age == 'latest':
        tmp_data_url = data_links[0].split("'")[1]
    elif age == 'random':
        tmp_data_url = random.randrange(0,len(data_links),1)

    data_file_name = tmp_data_url.split('/')[-1]
    base_data_url = links_to_data_url.replace('catalog.html',data_file_name)
    data_url = url_service_transform(base_data_url, from_service = 'catalog', to_service = service)

    return data_url
