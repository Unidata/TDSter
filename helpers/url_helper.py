__all__ = ['strip_date','get_latest_nam80_url']

def strip_date(x):
    '''
    A method to skip reading the date string from the datafile
    by simply returning -999 for that column of information.
    '''
    return -999

def get_latest_nam80_url(service = 'ncss'):
    ''''
    This function is used to retrieve the url on the motherlode
    THREDDS server for the latest NAM12 model run.

    Parameters
    ----------
    kind : string [odap, ncss]
        A string that describes the type of access service the user 
        wishes to use. Must be 'odap' or 'ncss'

    Returns
    -------
    data_url : string
        The URL that points to the datafile using the specified protocol.
    '''
    import urllib2

    base_data_url ="http://motherlode.ucar.edu/thredds/catalog/fmrc/NCEP/NAM/CONUS_80km/files/latest.html"

    ava_data = urllib2.urlopen(base_data_url)

    data_links = []
    for line in ava_data:
        if '<a href' in line:
            data_links.append(line)

    ava_data.close()

    latest_data = data_links[0].split("'")[1]
    data_file_name = latest_data.split('/')[-1]

    if service == 'odap':
        base_url = base_data_url.replace('/catalog/',
                    '/dodsC/grid/').replace('latest.html','')
    elif service == 'ncss':
        base_url = base_data_url.replace('/catalog/',
                    '/ncss/grid/').replace('latest.html','')

    data_url = base_url + data_file_name

    return data_url
