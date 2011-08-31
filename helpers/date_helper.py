import url_helper as uh
from string import join

__all__ = ['get_init_time','add_hours_to_init_time']

def get_init_time():
    filename = uh.get_latest_nam80_url().split('/')[-1].split('_')
    date_time = join([filename[3],filename[4][0:4]],'T')
    date_time = join([date_time,''],'Z')
    date_time = join([date_time[0:4], date_time[4:6],
                      date_time[6:]],'-')

    date_time = join([date_time[0:13],date_time[13:]],':00:')

    return date_time

def add_hours_to_init_time(init_time):
   return -999 
