﻿import url_helper as uh
from string import join
import datetime as dt
import time

__all__ = ['get_init_time']

def get_init_time():
    filename = uh.get_latest_nam80_url().split('/')[-1].split('_')
    # ['NAM', 'CONUS', '80km', '20120210', '0000.grib1']
    dateStr = filename[-2]
    timeStr = filename[-1].split('.')[0]
    timeFmt = '%Y%m%d%H%M'
    date_time = dt.datetime.fromtimestamp(time.mktime(time.strptime(join([dateStr,timeStr],''), timeFmt)))
    #date_time = join([filename[3],filename[4][0:4]],'T')
    #date_time = join([date_time,''],'Z')
    #date_time = join([date_time[0:4], date_time[4:6],
    #                  date_time[6:]],'-'
    #date_time = join([date_time[0:13],date_time[13:]],':00:')

    return date_time