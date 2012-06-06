import datetime as dt
import pydap.lib
import time

from pydap.client import open_url
from string import join

from url_helper import get_data_url
from http_helper import get_user_agent

__all__ = ['get_init_time', 'get_time_offset']

pydap.lib.USER_AGENT = get_user_agent()

def get_init_time():
    odap_url = get_data_url(service = 'odap')
    dataset = open_url(odap_url)

    if dataset.attributes['NC_GLOBAL'].has_key('_CoordinateModelRunDate'):
        dtstr = dataset.attributes['NC_GLOBAL']['_CoordinateModelRunDate']
        dtfmt = '%Y-%m-%dT%H:%M:%SZ'
        return dt.datetime.fromtimestamp(time.mktime(time.strptime(dtstr, dtfmt)))
    else:
        filename = get_data_url().split('/')[-1].split('_')
        # ['NAM', 'CONUS', '80km', '20120210', '0000.grib1']
        datestr = filename[-2]
        timestr = filename[-1].split('.')[0]
        timefmt = '%Y%m%d%H%M'
        date_time = dt.datetime.fromtimestamp(time.mktime(time.strptime(join([datestr,timestr],''), timefmt)))

        return date_time

def get_time_offset(time_index):
    odap_url = get_data_url(service = 'odap')
    dataset = open_url(odap_url)

    if dataset.has_key('time'):
        time_offset = dataset['time'][:][time_index]
        return dt.timedelta(hours = float(time_offset))
    else:
        print 'not implemented'